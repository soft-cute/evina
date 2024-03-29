use clap::Parser;
use logger_rust::log_error;
use std::{cell::RefCell, process::exit};
use tokio_retry::{strategy::FixedInterval, Retry};

#[tokio::main]
async fn main() {
    // 解析命令行参数
    let cli = evina_core::Cli::parse();
    // 设置重试策略
    let strategy = FixedInterval::from_millis(3000).take(cli.retry);
    // 判断cli的值
    match cli.live {
        Some(data) => {
            let retries: RefCell<i32> = RefCell::new(0);
            let result = Retry::spawn(strategy, || async {
                match data.as_str() {
                    "douyu" => match evina_core::live::douyu::get_rtmp_url(cli.id.clone()).await {
                        Ok(info) => Ok(info),
                        Err(e) => {
                            *retries.borrow_mut() += 1;
                            evina_core::retries(retries.clone());
                            Err(e)
                        }
                    },
                    "douyin" => match evina_core::live::douyin::get_rtmp_url(cli.id.clone()).await {
                        Ok(info) => Ok(info),
                        Err(e) => {
                            *retries.borrow_mut() += 1;
                            evina_core::retries(retries.clone());
                            Err(e)
                        }
                    },
                    _ => todo!(),
                }
            });
            match result.await {
                Ok(info) => evina_core::live::Information::print_information(&info).await,
                Err(e) => log_error!("Error: {}", e),
            };
        }
        None => match cli.config {
            true => {
                let list = vec!["DOUYU", "DOUYIN"];
                match cookie::read_config(cli.config_file.clone(), list) {
                    Ok(map) => evina_core::thread_run(map).await,
                    Err(e) => log_error!("{}", e),
                };
            }
            false => subcommand(cli).await,
        },
    }
}

async fn subcommand(cli: evina_core::Cli) {
    match cli.sub {
        Some(evina_core::Sub::Config { reload, add, del, list, symlink }) => match reload {
            true => cookie::live::reload(cli.config_file.clone()),
            false => match list {
                true => cookie::live::list(cli.config_file.clone()),
                false => match add {
                    Some(data) => cookie::live::add(cli.config_file, data),
                    None => match del {
                        Some(data) => cookie::live::del(cli.config_file, data),
                        None => match symlink {
                            Some(data) => cookie::live::symlink(cli.config_file, data),
                            None => exit(0),
                        },
                    },
                },
            },
        },
        Some(evina_core::Sub::History { live, id, date }) => match live {
            Some(live) => match live.as_str() {
                "douyu" => history::douyu(id, Some(date)).await,
                _ => todo!(),
            },
            None => exit(0),
        },
        None => exit(0),
    }
}

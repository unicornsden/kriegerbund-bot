use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::sync::mpsc::{self, Receiver, Sender, RecvError};
use std::thread;

use serenity::client::Client;
use serenity::model::channel::Message;
use serenity::prelude::{EventHandler, Context};
use std::sync::{Arc, Mutex};

enum ScanResult {
    Nothing,
    Message(Message)
}

unsafe impl Send for ScanResult {}
unsafe impl Sync for ScanResult {}

struct PixieScanner {
    sender: Arc<Mutex<Sender<ScanResult>>>,
    token : String
}

impl EventHandler for PixieScanner {
    fn message(&self, ctx: Context, msg: Message) {
        let sender = self.sender.lock().unwrap();
        sender.send(ScanResult::Message(msg));
    }
}

impl PixieScanner {
    fn new(
        sender: Sender<ScanResult>,
        token: &str) -> PixieScanner {
        let token = token.to_string();
        let sender = Arc::new(Mutex::new(sender));
        PixieScanner {
            sender,
            token
        }
    }
}

#[pyclass]
struct PyScanResult {
    result : u32
}

#[pyclass]
struct BackendHandle {
    receiver : Receiver<ScanResult>,
}

#[pyfunction]
fn start_scanning() -> PyResult<BackendHandle> {
    let (sender, receiver) : (Sender<ScanResult>, Receiver<ScanResult>)
        = mpsc::channel();

    thread::spawn(move || {
        let mut scanner = PixieScanner::new(
            sender,
            &"");
        let client = Client::new("".to_string(), scanner);
    });

    Ok(BackendHandle {
        receiver,
    })
}

#[pyfunction]
fn recv(handle : &BackendHandle) -> PyResult<PyScanResult> {
    let msg = recv_loop(handle);
    Ok((PyScanResult{ result : 0 }))
}

fn recv_loop(handle : &BackendHandle) -> Result<ScanResult, RecvError> {
    loop {
        let msg = handle.receiver.recv();
        match msg {
            Err(_) => {},
            _ => return msg
        }
    }
}

/// This module is a python module implemented in Rust.
#[pymodule]
fn pixie_backend(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(start_scanning))?;
    m.add_wrapped(wrap_pyfunction!(recv))?;
    Ok(())
}
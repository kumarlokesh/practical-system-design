//! A simple MNIST classifier example using our neural network implementation

use llm_from_scratch::{
    nn::{Linear, Module, ReLU, Sequential},
    Tensor,
};
use mnist::{Mnist, MnistBuilder};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    env_logger::init();

    // Load MNIST dataset
    let (trn_size, rows, cols) = (50_000, 28, 28);
    let (x_train, y_train, x_test, y_test) = load_mnist(trn_size)?;

    // Create a simple neural network
    let model = Sequential::new()
        .add(Linear::new(rows * cols, 128, true))
        .add(ReLU)
        .add(Linear::new(128, 10, true));

    println!("Model architecture:");
    println!("Input: {}x{} (flattened to {})", rows, cols, rows * cols);
    println!("  Linear(128) -> ReLU -> Linear(10)");

    // TODO: Add training loop
    println!("\nNote: Training loop not implemented yet.");

    Ok(())
}

fn load_mnist(
    trn_size: usize,
) -> Result<(Vec<Vec<f32>>, Vec<u8>, Vec<Vec<f32>>, Vec<u8>), Box<dyn std::error::Error>> {
    // Download and load MNIST dataset
    let (trn_size, val_size, tst_size) = (trn_size, 10_000, 10_000);

    let Mnist {
        trn_img,
        trn_lbl,
        val_img,
        val_lbl,
        tst_img,
        tst_lbl,
        ..
    } = MnistBuilder::new()
        .download_and_extract()
        .training_set_length(trn_size as u32)
        .validation_set_length(val_size as u32)
        .test_set_length(tst_size as u32)
        .finalize();

    // Convert images to f32 and normalize to [0, 1]
    let normalize = |x: u8| x as f32 / 255.0;

    // Reshape and normalize training data
    let x_train: Vec<Vec<f32>> = trn_img
        .chunks(28 * 28)
        .map(|chunk| chunk.iter().copied().map(normalize).collect())
        .collect();

    // Reshape and normalize test data
    let x_test: Vec<Vec<f32>> = tst_img
        .chunks(28 * 28)
        .map(|chunk| chunk.iter().copied().map(normalize).collect())
        .collect();

    Ok((x_train, trn_lbl, x_test, tst_lbl))
}

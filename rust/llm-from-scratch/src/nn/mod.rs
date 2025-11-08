//! Neural network modules and layers

mod activation;
mod linear;
mod sequential;

pub use activation::ReLU;
pub use linear::Linear;
pub use sequential::Sequential;

/// Common trait for all neural network layers
pub trait Module {
    /// Forward pass through the module
    fn forward(&self, input: &super::Tensor) -> super::Tensor;

    /// Get all trainable parameters
    fn parameters(&self) -> Vec<super::Tensor> {
        Vec::new()
    }
}

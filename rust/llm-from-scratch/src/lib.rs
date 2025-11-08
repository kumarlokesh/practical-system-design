//! A from-scratch implementation of neural networks and eventually a full LLM in Rust.
//!
//! This crate provides the building blocks for creating and training neural networks,
//! with the ultimate goal of building a full language model.

#![warn(missing_docs)]

pub mod nn;
pub mod tensor;

// Re-export commonly used items
pub use nn::{activation::ReLU, linear::Linear, sequential::Sequential, Module};
pub use tensor::Tensor;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_imports() {
        // Just check that we can import everything
        let _: Tensor = Tensor::zeros((2, 2), false);
        let _: Linear = Linear::new(10, 5, true);
        let _: ReLU = ReLU;
        let _: Sequential = Sequential::new();
    }
}

//! A simple tensor implementation for neural networks

use ndarray::{Array, ArrayD, IxDyn};
use std::ops::{Add, AddAssign, Mul, Sub};

/// A multi-dimensional array that supports basic operations needed for neural networks
#[derive(Debug, Clone)]
pub struct Tensor {
    data: ArrayD<f32>,
    requires_grad: bool,
    // TODO: Add gradient tracking for autodiff
}

impl Tensor {
    /// Create a new tensor from an array
    pub fn new(data: ArrayD<f32>, requires_grad: bool) -> Self {
        Self {
            data,
            requires_grad,
        }
    }

    /// Create a tensor filled with zeros with the given shape
    pub fn zeros<D: ndarray::Dimension>(shape: D, requires_grad: bool) -> Self {
        Self::new(Array::zeros(shape).into_dyn(), requires_grad)
    }

    /// Create a tensor filled with ones with the given shape
    pub fn ones<D: ndarray::Dimension>(shape: D, requires_grad: bool) -> Self {
        Self::new(Array::ones(shape).into_dyn(), requires_grad)
    }

    /// Create a tensor with random values in [0, 1) with the given shape
    pub fn rand<D: ndarray::Dimension>(shape: D, requires_grad: bool) -> Self {
        use ndarray_rand::rand_distr::Uniform;
        use ndarray_rand::RandomExt;

        let dist = Uniform::new(0.0, 1.0);
        Self::new(Array::random(shape, dist).into_dyn(), requires_grad)
    }

    /// Get the shape of the tensor
    pub fn shape(&self) -> &[usize] {
        self.data.shape()
    }

    /// Get a reference to the underlying array data
    pub fn data(&self) -> &ArrayD<f32> {
        &self.data
    }

    /// Get a mutable reference to the underlying array data
    pub fn data_mut(&mut self) -> &mut ArrayD<f32> {
        &mut self.data
    }

    /// Matrix multiplication (dot product) with another tensor
    pub fn matmul(&self, other: &Tensor) -> Self {
        // TODO: Add shape checking
        let result = self.data.dot(&other.data);
        Self::new(result, self.requires_grad || other.requires_grad)
    }

    /// Element-wise addition
    pub fn add(&self, other: &Tensor) -> Self {
        let result = &self.data + &other.data;
        Self::new(result, self.requires_grad || other.requires_grad)
    }

    /// Element-wise multiplication
    pub fn mul(&self, other: &Tensor) -> Self {
        let result = &self.data * &other.data;
        Self::new(result, self.requires_grad || other.requires_grad)
    }

    /// Apply ReLU activation function
    pub fn relu(&self) -> Self {
        let result = self.data.mapv(|x| if x > 0.0 { x } else { 0.0 });
        Self::new(result, self.requires_grad)
    }
}

// Implement basic arithmetic operations
impl Add for &Tensor {
    type Output = Tensor;

    fn add(self, other: Self) -> Self::Output {
        self.add(other)
    }
}

impl Add<f32> for &Tensor {
    type Output = Tensor;

    fn add(self, scalar: f32) -> Self::Output {
        let result = &self.data + scalar;
        Tensor::new(result, self.requires_grad)
    }
}

impl Mul for &Tensor {
    type Output = Tensor;

    fn mul(self, other: Self) -> Self::Output {
        self.mul(other)
    }
}

impl Mul<f32> for &Tensor {
    type Output = Tensor;

    fn mul(self, scalar: f32) -> Self::Output {
        let result = &self.data * scalar;
        Tensor::new(result, self.requires_grad)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_creation() {
        let t = Tensor::zeros((2, 3), false);
        assert_eq!(t.shape(), &[2, 3]);
        assert_eq!(t.data().sum(), 0.0);
    }

    #[test]
    fn test_tensor_addition() {
        let a = Tensor::ones((2, 2), false);
        let b = Tensor::ones((2, 2), false);
        let c = &a + &b;
        assert_eq!(c.data().sum(), 8.0); // 2x2 matrix of 2.0s
    }

    #[test]
    fn test_tensor_multiplication() {
        let a = Tensor::ones((2, 2), false);
        let b = &a * 2.0;
        assert_eq!(b.data().sum(), 8.0); // 2x2 matrix of 2.0s
    }
}

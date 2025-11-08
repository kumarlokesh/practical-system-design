use super::Module;
use crate::Tensor;

/// A linear (fully connected) layer
#[derive(Debug)]
pub struct Linear {
    weights: Tensor,
    bias: Option<Tensor>,
}

impl Linear {
    /// Create a new linear layer with the given input and output dimensions
    pub fn new(input_dim: usize, output_dim: usize, use_bias: bool) -> Self {
        // Initialize weights with He initialization
        let scale = (2.0 / input_dim as f32).sqrt();
        let weights = Tensor::rand((input_dim, output_dim), true) * scale;

        let bias = if use_bias {
            Some(Tensor::zeros(output_dim, true))
        } else {
            None
        };

        Self { weights, bias }
    }
}

impl Module for Linear {
    fn forward(&self, input: &Tensor) -> Tensor {
        let output = input.matmul(&self.weights);

        match &self.bias {
            Some(bias) => output + bias,
            None => output,
        }
    }

    fn parameters(&self) -> Vec<Tensor> {
        let mut params = vec![self.weights.clone()];
        if let Some(bias) = &self.bias {
            params.push(bias.clone());
        }
        params
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use approx::assert_relative_eq;

    #[test]
    fn test_linear_forward() {
        let linear = Linear::new(3, 2, true);
        let input = Tensor::ones((1, 3), false);
        let output = linear.forward(&input);

        assert_eq!(output.shape(), &[1, 2]);

        // Check that the output is not all zeros (weights are randomly initialized)
        assert!(
            output.data().sum() != 0.0,
            "Linear layer output should not be all zeros"
        );
    }
}

use super::Module;
use crate::Tensor;

/// ReLU activation function
#[derive(Debug, Default)]
pub struct ReLU;

impl Module for ReLU {
    fn forward(&self, input: &Tensor) -> Tensor {
        input.relu()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::array;

    #[test]
    fn test_relu() {
        let relu = ReLU;
        let input = Tensor::new(array![[-1.0, 0.0, 1.0]].into_dyn(), false);
        let output = relu.forward(&input);

        let expected = array![[0.0, 0.0, 1.0]].into_dyn();
        assert_eq!(output.data(), &expected);
    }
}

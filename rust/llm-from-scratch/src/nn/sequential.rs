use super::Module;
use crate::Tensor;

/// A sequential container that applies a series of modules in order
#[derive(Default)]
pub struct Sequential {
    modules: Vec<Box<dyn Module>>,
}

impl Sequential {
    /// Create a new empty sequential container
    pub fn new() -> Self {
        Self {
            modules: Vec::new(),
        }
    }

    /// Add a module to the container
    pub fn add<M: Module + 'static>(mut self, module: M) -> Self {
        self.modules.push(Box::new(module));
        self
    }
}

impl Module for Sequential {
    fn forward(&self, input: &Tensor) -> Tensor {
        let mut output = input.clone();
        for module in &self.modules {
            output = module.forward(&output);
        }
        output
    }

    fn parameters(&self) -> Vec<Tensor> {
        let mut params = Vec::new();
        for module in &self.modules {
            params.extend(module.parameters());
        }
        params
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::nn::{Linear, ReLU};

    #[test]
    fn test_sequential() {
        let model = Sequential::new()
            .add(Linear::new(10, 20, true))
            .add(ReLU)
            .add(Linear::new(20, 2, true));

        let input = Tensor::ones((1, 10), false);
        let output = model.forward(&input);

        assert_eq!(output.shape(), &[1, 2]);

        // Check that we can get all parameters
        let params = model.parameters();
        assert_eq!(params.len(), 4); // 2 layers * (weights + bias)
    }
}

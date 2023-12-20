use crate::allocator::rlocint::RlocInt;
use pyo3::prelude::*;
use std::sync::Arc;

// use crate::rlocint::RlocInt;

// div_floor is not stabilized yet
trait DivFloor {
    fn div_floor(&self, rhs: i32) -> i32;
}

impl DivFloor for i32 {
    fn div_floor(&self, rhs: i32) -> i32 {
        if rhs < 0 {
            -((-self).div_euclid(rhs))
        } else {
            self.div_euclid(rhs)
        }
    }
}

#[pyclass(frozen, subclass)]
pub struct ConstExpr {
    baseobj: Option<Arc<ConstExpr>>,
    offset: i32,
    rlocmode: i32,
}

#[pymethods]
impl ConstExpr {
    #[new]
    #[pyo3(signature = (baseobj, offset=0, rlocmode=4))]
    fn new(baseobj: Option<&ConstExpr>, offset: i32, rlocmode: i32) -> Self {
        Self {
            baseobj: baseobj.map_or(None, |expr| expr.baseobj.clone()),
            offset,
            rlocmode,
        }
    }
}
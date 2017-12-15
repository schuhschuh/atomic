#include <atomic>
#include <pybind11/pybind11.h>

namespace py = pybind11;


class AtomicLong
{
    std::atomic<long> value_;

public:

    AtomicLong(long value = 0) : value_(value) {}

    void setValue(long value)
    {
        value_ = value;
    }

    long getValue() const
    {
        return value_;
    }

    long getAndSet(long value)
    {
        return value_.exchange(value);
    }

    bool compareAndSet(long expected, long value)
    {
        return value_.compare_exchange_strong(expected, value);
    }

    void add(long value)
    {
        value_ += value;
    }

    void sub(long value)
    {
        value_ -= value;
    }
};


PYBIND11_MODULE(detail, m) {
    py::class_<AtomicLong>(m, "AtomicLong")
        .def(py::init<>())
        .def(py::init<long>())
        .def_property("value", &AtomicLong::getValue, &AtomicLong::setValue)
        .def("add", &AtomicLong::add)
        .def("sub", &AtomicLong::sub)
        .def("get_and_set", &AtomicLong::getAndSet, "Atomically sets to the given value and returns the old value\n\n:param new_value: the new value")
        .def("compare_and_set", &AtomicLong::compareAndSet, "Atomically sets the value to the given value if the current value is equal to the expected value.\n\n:param expect_value: the expected value\n:param new_value: the new value");
}

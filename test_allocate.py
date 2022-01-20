from datetime import date, timedelta

from models import Batch, OrderLine, allocate


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment_batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1))
    line = OrderLine("oref", "RETRO-CLOCK", 10)
    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100

def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=date.today())
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=date.today() + timedelta(days=1))
    latest = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=date.today() + timedelta(weeks=1))
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)
    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100

def test_returns_allocated_batch_ref():
    in_stack_batch = Batch("in-stack-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("in-stack-batch-ref", "HIGHBROW-POSTER", 100, eta=date.today() + timedelta(days=1))
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stack_batch, shipment_batch])
    assert allocation == in_stack_batch.reference

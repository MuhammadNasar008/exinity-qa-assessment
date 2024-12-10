import time

import grpc
import pytest

from src import chart_service_pb2, chart_service_pb2_grpc
from database.db_operations import get_last_candlestick  # Import for database validation

def test_candlestick_generation():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD"]
        )

        # Send the request and get the streaming responses
        responses = stub.Subscribe(request)
        for response in responses:
            # Validate the gRPC response fields
            assert response.symbol == "EURUSD", "Symbol mismatch in response"
            assert response.bar.timestamp_msec > 0, "Invalid timestamp"
            assert response.bar.open > 0, "Open price must be greater than 0"
            assert response.bar.high >= response.bar.low, "High must be greater than or equal to Low"

            # Validate the candlestick data against the database
            db_candle = get_last_candlestick(response.symbol)
            if db_candle:
                assert db_candle['timestamp_msec'] < response.bar.timestamp_msec, (
                    "New candlestick must have a greater timestamp than the last one in the database"
                )

def test_multiple_symbols():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD", "GBPUSD"]
        )
        responses = stub.Subscribe(request)
        for response in responses:
            assert response.symbol in ["EURUSD", "GBPUSD"]
            assert response.bar.timestamp_msec > 0
            assert response.bar.open > 0

def test_duplicate_check():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD"]
        )
        responses = stub.Subscribe(request)
        for response in responses:
            db_candle = get_last_candlestick(response.symbol)
            if db_candle:
                assert db_candle['timestamp_msec'] < response.bar.timestamp_msec

def test_broadcasting():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD"]
        )
        responses = stub.Subscribe(request)
        for response in responses:
            assert response.symbol == "EURUSD"
            assert response.bar.timestamp_msec > 0

def test_no_overlap():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD"]
        )
        previous_timestamp = None
        responses = stub.Subscribe(request)
        for response in responses:
            if previous_timestamp:
                assert response.bar.timestamp_msec > previous_timestamp
            previous_timestamp = response.bar.timestamp_msec

def test_timeframe():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chart_service_pb2_grpc.ChartServiceStub(channel)
        request = chart_service_pb2.SubscribeRequest(
            timeframe=chart_service_pb2.TIMEFRAME_MINUTE_1,
            symbol_list=["EURUSD"]
        )
        responses = stub.Subscribe(request)
        for response in responses:
            assert response.bar.timestamp_msec % 60000 == 0  # Must be divisible by 60 seconds (1 minute)







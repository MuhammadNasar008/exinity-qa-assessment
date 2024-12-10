import time
import grpc
from concurrent import futures
from src import chart_service_pb2, chart_service_pb2_grpc


# Mock data for responses
MOCK_CANDLESTICKS = {
    "EURUSD": [
        chart_service_pb2.Candlestick(
            timestamp_msec=1672502400000,  # Example timestamp
            open=1.1000,
            high=1.2000,
            low=1.0900,
            close=1.1500,
        )
    ]
}

class ChartService(chart_service_pb2_grpc.ChartServiceServicer):
    def Subscribe(self, request, context):
        # Simulate streaming candlesticks for the requested symbols
        for symbol in request.symbol_list:
            for candle in MOCK_CANDLESTICKS.get(symbol, []):
                yield chart_service_pb2.SubsribeResponse(
                    symbol=symbol,
                    bar=candle,
                )
                time.sleep(1)  # Simulate a delay in the stream

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chart_service_pb2_grpc.add_ChartServiceServicer_to_server(ChartService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    serve()

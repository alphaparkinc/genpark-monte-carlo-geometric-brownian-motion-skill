import sys, json
from client import MonteCarloGBMSimulator

sim = MonteCarloGBMSimulator()

def handle_jsonrpc(line):
    global sim
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-monte-carlo-geometric-brownian-motion-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "simulate_gbm", "description": "Run Monte Carlo GBM simulation.", "inputSchema": {"type": "object", "properties": {"S0": {"type": "number"}, "mu": {"type": "number"}, "sigma": {"type": "number"}, "T": {"type": "number"}}, "required": ["S0", "mu", "sigma", "T"]}},
                {"name": "benchmark_monte_carlo_gbm", "description": "Run benchmark simulation.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "simulate_gbm":
                res = sim.simulate_paths(args.get("S0"), args.get("mu"), args.get("sigma"), args.get("T"))
            elif tool == "benchmark_monte_carlo_gbm":
                res = sim.benchmark_monte_carlo_gbm()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()

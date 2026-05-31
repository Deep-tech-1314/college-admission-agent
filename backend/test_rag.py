import asyncio
from rag_pipeline import initialize_rag, query_agent

def test():
    print("Testing initialization...")
    initialize_rag()
    print("\nTesting query...")
    result = query_agent("What is the fee structure for undergraduate students?")
    print("\nAnswer:")
    print(result.get("answer"))
    print("\nSources:")
    for src in result.get("sources", []):
        print("-", src)

if __name__ == "__main__":
    test()

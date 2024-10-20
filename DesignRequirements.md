**FastAPI Service for an Optimized LLM with a Medusa Head**

### **Objective:**

Implement a FastAPI service that serves a Language Model (LLM) with a [medusa](https://github.com/FasterDecoding/Medusa) head (using lmsys/vicuna-7b). The goal is to optimize the inference speed using a model compilation library (e.g., llama.cpp) and enhance performance via speculative decoding with the medusa head. Additionally, you are required to implement dynamic batching to handle multiple concurrent requests efficiently.

### **Key Deliverables:**

1. **Model Compilation:**
    - Use a model compilation library (e.g., [llama.cpp](https://github.com/ggerganov/llama.cpp)) to optimize the inference of the base model.
    - Provide an explanation of your choice of compilation library and its impact on performance.
2. **Medusa Head Implementation:**
    - Implement the medusa head on top of the base model to improve performance via speculative decoding. Avoid using existing implementations.
    - Include a brief explanation of how speculative decoding is implemented and its advantages.
3. **Dynamic Batching:**
    - Implement dynamic batching to efficiently manage multiple concurrent requests.
    - Explain your approach to dynamic batching and its benefits in serving LLMs.
4. **Service Implementation:**
    - Use [FastAPI](https://fastapi.tiangolo.com/) to create a service that serves the LLM with the medusa head.
    - Ensure the service can handle concurrent requests with low latency.
5. **Testing & Validation:**
    - Provide test cases to validate the correctness and efficiency of your implementation.
    - Include performance benchmarks or metrics comparing different configurations (e.g., with and without the medusa head, with and without dynamic batching).
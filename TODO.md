### API Changes ###

- [ ] Python packaging
- [x] Dockerfile
- [ ] Split into model, celery and API into microservices

### Design additions ###
- [ ] Load balancer
- [ ] Cache
- [ ] Model config is static, watch config or load models dynamically (need to watch available resources)

### Makefile ###
- [ ] Add commands to fetch and convert models

#### Fixes ###
- [ ] TTL to env

### Others ###
- [ ] Add medusa head
- [ ] Add proper dynamic batching, currently we are using redis to mimic batching
- [ ] Need to do benchmarking with different quantization models, medusa, (proper) dyn batching abd speculative decoding

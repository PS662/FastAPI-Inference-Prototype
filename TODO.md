### API Changes ###

- [ ] Python packaging
- [ ] Dockerfile
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
- [ ] Add proper dynamic batching, currently we are using redis to mimin batching

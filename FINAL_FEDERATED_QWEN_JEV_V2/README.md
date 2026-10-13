# Federated Qwen + JEV Decision Intelligence — V2

Architecture:

Agent 1
   ↓
Local Qwen + LoRA
   ↓
Agent 2
   ↓
Local Qwen + LoRA
   ↓
FedAvg
   ↓
Global Qwen
   ↓
Natural-language explanation
   ↓
JEV-9B System 1
   ↓
Structured decision + probability

Included:

qwen/agent1
qwen/agent2
qwen/global_qwen

jev/head.safetensors
jev/calibration.json
jev/adapter
jev/adapter_vllm

The base Qwen and full JEV-9B model weights are not duplicated
because they are large base-model dependencies.

Raw training data is not included.

The Global Qwen adapter is produced from the synchronized
two-agent FedAvg round.
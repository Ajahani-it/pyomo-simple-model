"""
Copyright 2018 Eugenio Gianniti

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pyomo.environ as pe

import parts

model = pe.AbstractModel(name="Single node")

# Sets
model.VMs = parts.VMs
model.Jobs = parts.Jobs

# Parameterized sets :)
model.available_GPUs = parts.available_GPUs
model.GPUs = parts.GPUs
model.VM_GPU_pairs = parts.VM_GPU_pairs

# Parameters
model.time = parts.time
model.cost = parts.cost
model.deadline = parts.deadline
model.penalty = parts.penalty
model.tardinessweight = parts.tardinessweight

# Variables
model.deployment = parts.deployment
model.chosen_VMs = parts.chosen_VMs
model.final_cost = parts.final_cost
model.tardiness = parts.tardiness
model.chosen_job = parts.chosen_job

# Constraints
model.one_VM = parts.one_VM
model.disable_VMs = parts.disable_VMs
model.one_deployment = parts.one_deployment
model.GPU_bound = parts.GPU_bound
model.job_duration = parts.job_duration
model.maximum_deployed_cost = parts.maximum_deployed_cost
model.selected_VM_for_not_rejectedjob = parts.selected_VM_for_not_rejectedjob


# Objective
model.minimum_cost = parts.minimum_cost

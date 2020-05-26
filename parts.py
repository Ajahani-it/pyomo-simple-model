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

# Sets
"V"
VMs = pe.Set(doc="VM models")
"J"
Jobs = pe.Set(doc="Submitted jobs")
"G_v"
GPUs = pe.Set(VMs, initialize=lambda model, v: range(1, model.available_GPUs[v] + 1),
              within=pe.NonNegativeIntegers, doc="GPU numbers")
"""
Indexed sets can't be used as indices for other entities, hence we must
create an auxiliary set of pairs that is flat and 2D.
"""
VM_GPU_pairs = pe.Set(dimen=2, doc="Relevant VM/GPU pairs",
                      initialize=lambda model:
                      ((v, g) for v in model.VMs for g in model.GPUs[v]))

# Parameters
"n_v"
available_GPUs = pe.Param(VMs, within=pe.NonNegativeIntegers, doc="Number of GPUs available on VM v")
"c_v"
cost = pe.Param(VMs, within=pe.NonNegativeReals, doc="Time unit cost for running VM v")
"d_j"
deadline = pe.Param(Jobs, within=pe.NonNegativeReals, doc="Deadline of job j")
"p_j"
penalty = pe.Param(Jobs, within=pe.NonNegativeReals, doc="Penalty of job j")
"w_j"
tardinessweight = pe.Param(Jobs, within=pe.NonNegativeReals, doc="Tardiness Weight of job j")

"t_{j v g}"
time = pe.Param(Jobs, VM_GPU_pairs, within=pe.NonNegativeReals,
                doc="Execution time of job j on VM v with g GPUs")

# Variables
"x_{j v g}"
deployment = pe.Var(Jobs, VM_GPU_pairs, within=pe.Boolean,
                    doc="True if job j runs on VM v with g GPUs")
"y_v"
chosen_VMs = pe.Var(VMs, within=pe.Boolean, doc="True if VM v is switched on")
"τ_j"
tardiness = pe.Var (Jobs, within=pe.NonNegativeReals, doc="tardiness of job j")
"z_j"
chosen_job = pe.Var (Jobs, within=pe.Boolean, doc="job j is selected")

"ξ"
final_cost = pe.Var(within=pe.NonNegativeReals, doc="Minimum total cost")

# Constraints
"(P1b)"
one_VM = pe.Constraint(doc="Enable only one node",
                       rule=lambda model: pe.summation(model.chosen_VMs) == 1)
"(P1c)"
disable_VMs = pe.Constraint(Jobs, VM_GPU_pairs,
                            doc="Disable all the choices related to discarded VMs",
                            rule=lambda model, j, v, g:
                            model.deployment[j, v, g] <= model.chosen_VMs[v])
"(P1d)"
one_deployment = pe.Constraint(Jobs, doc="Enforce exactly one deployment per job",
                               rule=lambda model, j:
                               sum(model.deployment[j, v, g]
                                   for v in model.VMs for g in model.GPUs[v]) == model.chosen_job[j])
"(P1e)"
GPU_bound = pe.Constraint(VMs, doc="Constrain the number of GPUs available per VM",
                          rule=lambda model, v:
                          sum(g * model.deployment[j, v, g]
                              for j in model.Jobs for g in model.GPUs[v]) <= model.available_GPUs[v])
"(P1f)"
job_duration = pe.Constraint(Jobs, doc="Enforce deadlines on jobs",
                             rule=lambda model, j:
                             sum(model.time[j, v, g] * model.deployment[j, v, g]
                                 for v in model.VMs for g in model.GPUs[v]) <= model.deadline[j]+model.tardiness[j])
"(P1g)"
maximum_deployed_cost = pe.Constraint(Jobs, VM_GPU_pairs, doc="Find maximum total cost among deployed jobs",
                                      rule=lambda model, j, v, g:
                                      model.final_cost >=
                                      model.time[j, v, g] * model.cost[v] * model.deployment[j, v, g])

"(p1h)"
selected_VM_for_not_rejectedjob = pe.Constraint(Jobs, VM_GPU_pairs, doc="Find selected VM is for a not rejected job",
                                                rule=lambda model, j, v, g:
                                                    model.deployment[j, v, g] <= model.chosen_job[j])    

# Objectives
"(P1a)"
minimum_cost = pe.Objective(doc="Minimize execution time based on deployment",
                            rule=lambda model: model.final_cost+sum(model.penalty[j]*(1-model.chosen_job[j]) for j in model.Jobs)+sum(model.tardinessweight[j]*model.tardiness[j] for j in model.Jobs))

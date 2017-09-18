import { get, post } from './api'

export async function supervisorServicesList (supervisorId) {
  let list = (await (await get(`/monitor/api/supervisor/${supervisorId}/prog/`)).json()).data
  return list
}

export async function supervisorServiceStop (supervisorId, name) {
  let res = await (await post(`/monitor/api/supervisor/${supervisorId}/prog/${name}/stop/`).json()).data
  return res
}

export async function supervisorServiceStart (supervisorId, name) {
  let res = await (await post(`/monitor/api/supervisor/${supervisorId}/prog/${name}/start/`).json()).data
  return res
}

export async function supervisorServiceRestart (supervisorId, name) {
  let res = await (await post(`/monitor/api/supervisor/${supervisorId}/prog/${name}/restart/`).json()).data
  return res
}


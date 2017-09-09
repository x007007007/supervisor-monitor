import { get } from './api'

export async function supervisorServicesList (supervisorId) {
  let list = (await (await get(`/monitor/api/supervisor/${supervisorId}/prog/`)).json()).data
  return list
}

export async function supervisorServiceStop (supervisorId, name) {
  console.log(`stop ${supervisorId}, ${name}`)
}

export async function supervisorIdServiceStart (supervisorId, name) {
  console.log(`start ${supervisorId}, ${name}`)
}

export async function supervisorServiceRestart (supervisorId, name) {
  console.log(`restart ${supervisorId}, ${name}`)
}


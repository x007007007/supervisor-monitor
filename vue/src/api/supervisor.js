import { get } from './api'

export async function supervisorListApi (supervisorId) {
  let list = (await (await get(`/monitor/api/supervisor/`)).json()).data
  let res = []
  for (let item of list) {
    switch (item.state) {
      case -1:
        item.state_name = 'SHUTDOWN'
        break
      case 0:
        item.state_name = 'RESTARTING'
        break
      case 1:
        item.state_name = 'RUNNING'
        break
      case 2:
        item.state_name = 'FATAL'
        break
      default:
        item.state_name = 'UNKNOWN'
    }
    res.push(item)
  }
  return res
}

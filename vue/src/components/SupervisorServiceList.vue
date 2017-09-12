<i18n>
en:
  STOPPED: "STOPPED"
  STARTING: "STARTING"
  RUNNING: "RUNNING"
  BACKOFF: "BACKOFF"
  STOPPING: "STOPPING"
  FATAL: "FATAL"
  EXITED: "EXITED"
  UNKNOWN: "UNKNOWN"
zh_CN:
  STOPPED: "停止的"
  STARTING: "启动中"
  RUNNING: "运行中"
  BACKOFF: "重试准备"
  STOPPING: "停止中"
  FATAL: "实效"
  EXITED: "退出"
  UNKNOWN: "为止"
</i18n>

<template>
  <div class="list supervisor-service-list">
    <ul>
      <li v-for="item in service_list">
        {{ item.status }}
        {{ item.exit_status }}
        {{ item.name }}
        {{ item.group }}
        {{ item.pid }}
        {{ item.state }}
        {{ item.start_timestamp }}
        {{ item.now_timestamp }}
        <button v-on:click="restart(item.name)">restart</button>
        <button v-on:click="stop(item.name)">stop</button>
        <button v-on:click="start(item.name)">start</button>
      </li>
    </ul>
  </div>
</template>

<script>
  import { supervisorServicesList, supervisorServiceStop, supervisorServiceRestart, supervisorServiceStart } from '@/api/supervisorService'

  export default {
    props: {
      supervisor_id: String
    },
    data: () => {
      return {
        service_list: []
      }
    },
    methods: {
      async refresh () {
        if (this.supervisor_id) {
          this.service_list = await supervisorServicesList(this.supervisor_id)
        } else {
          this.service_list = []
        }
      },
      async start (name) {
        supervisorServiceStart(this.supervisor_id, name)
      },
      async stop (name) {
        supervisorServiceStop(this.supervisor_id, name)
      },
      async restart (name) {
        supervisorServiceRestart(this.supervisor_id, name)
      }
    },
    mounted: function () {
      this.refresh()
    }
  }
</script>

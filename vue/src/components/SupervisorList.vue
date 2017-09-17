<i18n>
en:
  SHUTDOWN: "SHUTDOWN!"
  FATAL: "FATAL"
  RESTARTING: "RESTARTING"
  RUNNING: "RUNNING"
  OFFLINE: "OFFLINE"
  state: "state"
zh_CN:
  SHUTDOWN: "关闭"
  FATAL: "失败"
  RESTARTING: "重启中"
  RUNNING: "运行中"
  OFFLINE: "离线"
  state: "状态"
</i18n>

<template>
  <div class="supervisor_list">
    <button class="refresh" v-on:click="refresh">refresh</button>
    <ul>
      <li class="supervisor" v-for="sinfo in supervisor_list" >
        <div class="info">
          <p>
            <span class="identification">{{ sinfo.identification }}</span>
            <span class="ip" v-show="sinfo.ip">({{ sinfo.ip }})</span>
          </p>
          <p>
            <span class="pid"> PID: {{ sinfo.pid }}</span>
            <span class="state">{{ $t('state') }}:{{ $t(sinfo.state_name) }}</span>
          </p>
          <button class="more" v-on:click="selectedById(sinfo.identification)" v-show="clicked != sinfo.identification">more</button>
          <button class="less" v-on:click="selectedById(null)" v-show="clicked == sinfo.identification">less</button>
        </div>
        <service-list :supervisor_id="sinfo.identification" v-show="clicked == sinfo.identification"></service-list>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="stylus">
  body
    padding: 0;
    margin: 0;
    div.supervisor_list
      position: relative;
      width: 300px;
      height: 100%;
      padding-top: 32px;
      button.refresh
        position: absolute;
        top: 0px;
        right: 0px;
        text-indent: -9999999999px;
        background-color: #4CAF50; /* Green */
        width: 32px;
        height: 32px;
      ul
        li.supervisor
          list-style-type: none;
          div.info
            position: relative;
            top: 0;
            right: 0;
            width: 300px;
            height: 100px;
            border: solid 1px;
            button.more, button.less
              width: 100%;
              position: absolute;
              bottom: 0px;
              right: 0px;
</style>

<script>
  import { supervisorListApi } from '@/api/supervisor'

  export default {
    props: {
      selected: String
    },
    components: {
      'service-list': () => import('@/components/SupervisorServiceList')
    },
    data: () => {
      return {
        locale: 'zh_CN',
        supervisor_list: [],
        clicked: this.selected
      }
    },
    methods: {
      async refresh () {
        this.supervisor_list = await supervisorListApi()
      },
      selectedById (identification) {
        this.clicked = identification
      }
    },
    mounted: function () {
      this.$i18n.locale = 'zh_CN'
      this.refresh()
    },
    watch: {
      locale (val) {
        console.log(val)
        this.$i18n.locale = val
      }
    }
  }
</script>



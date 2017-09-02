<template>
  <div class="supervisor_list">
    <button v-on:click="refresh">refresh</button>
    <ul>
      <li v-for="sinfo in supervisor_list">
          <span class="identification">{{ sinfo.identification }}</span>
          <span class="ip">{{ sinfo.ip }}</span>
          <span class="pid">{{ sinfo.pid }}</span>
      </li>
    </ul>
  </div>
</template>


<script>
  export default {
    state: {
      supervisor_list: null
    },
    data: () => {
      return {
        supervisor_list: []
      }
    },
    methods: {
      async refresh () {
        this.supervisor_list = (await (await fetch('http://127.0.0.1:8000/monitor/api/supervisor/')).json()).data
      }
    },
    mounted: function () {
      this.refresh()
    }
  }
</script>


<style lang="stylus">

</style>

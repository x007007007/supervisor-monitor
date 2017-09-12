<template>
  <div class="row">
    <supervisor-list :selected.sync="supervisor_id" ></supervisor-list>
    <service-list :sueprvisor_id="supervisor_id"></service-list>
  </div>
</template>


<script>
  export default {
    data: () => {
      return {
        supervisor_id: null
      }
    },
    components: {
      'supervisor-list': () => import('@/components/SupervisorList'),
      'service-list': () => import('@/components/SupervisorServiceList')
    }
  }
</script>


<style scoped lang="stylus">

</style>

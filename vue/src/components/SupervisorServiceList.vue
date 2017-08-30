<template>
  <div class="list supervisor-service-list">
    <ul>
      <li v-for="item in service_list">
        {{ supervisor_list.status }}
        <service-log-print></service-log-print>
        <service-console></service-console>
      </li>
    </ul>
  </div>
</template>

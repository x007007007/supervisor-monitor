<template>
  <div class="list supervisor-list">
    <ul>
      <li v-for="item in supervisor_list">
        {{ supervisor_list.status }}
        <supervisor-service-list></supervisor-service-list>
      </li>
    </ul>
  </div>
</template>

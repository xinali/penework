<template>
    <p> {{ msg }} </p>
</template>


<script>
export default {
  name: 'NotAuth',
  data() {
    return {
      msg: '401 page'
    }
  }
}

<template lang="pug">
b-navbar(toggleable="lg" dark variant="dark")
  b-navbar-brand(to="/") BirdCAGE
  b-navbar-toggle(target="nav-collapse")
  b-collapse.navbar-collapse(id="nav-collapse" is-nav)
    b-navbar-nav
      b-nav-item(to="/recent-detections") Recent Detectinos
      b-nav-item(to="/streams") Streams
</template>
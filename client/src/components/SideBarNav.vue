<template>
    <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
            <li class="nav-item nav-profile">
                <router-link to="/" class="nav-link">
                    <div class="nav-profile-image">
                        <img src="https://placebeard.it/128x128" alt="profile" />
                        <span class="login-status online"></span>
                        <!--change to offline or busy as needed-->
                    </div>
                    <div class="nav-profile-text d-flex flex-column">
                        <span
                            class="font-weight-bold mb-2"
                        >{{ this.$store.state.user.fullName }}</span>
                        <span class="text-secondary text-small">Beard Manager</span>
                    </div>
                    <i class="mdi mdi-bookmark-check text-success nav-profile-badge"></i>
                </router-link>
            </li>
            <li class="nav-item" v-if="false">
                <router-link class="nav-link" to="/debug">
                    <span class="menu-title">Debug</span>
                    <i class="mdi mdi-bug menu-icon"></i>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/bitchns">
                    <span class="menu-title">DNS Config</span>
                    <i class="mdi mdi-dns menu-icon"></i>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/myip">
                    <span class="menu-title">My IP Address</span>
                    <i class="mdi mdi-ip menu-icon"></i>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/jwt">
                    <span class="menu-title">JWT Decoder</span>
                    <i class="mdi mdi-code-array menu-icon"></i>
                </router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/lights">
                    <span class="menu-title">Lights</span>
                    <i class="mdi mdi-lightbulb menu-icon"></i>
                </router-link>
            </li>
        </ul>
    </nav>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class SideBarNav extends Vue {

}
</script>

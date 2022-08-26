<template>
  <div
    class="modal fade"
    id="addUser"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">Add New User</h5>
          <button
            type="button"
            class="btn btn-sm"
            data-bs-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body px-5 pt-5">
          <form @submit.prevent="createUser()">
            <div class="row mb-4">
              <div class="form-group col-md-6">
                <label>Email</label>
                <input type="email" class="form-control" v-model="email" />
              </div>
              <div class="form-group col-md-6">
                <label for="">Username</label>
                <input type="text" class="form-control" v-model="username" />
              </div>
            </div>
            <div class="row mb-4">
              <div class="form-group col-md-4">
                <label for="">First Name</label>
                <input type="text" class="form-control" v-model="first_name" />
              </div>
              <div class="form-group col-md-4">
                <label for="">Middle Name</label>
                <input type="text" class="form-control" v-model="middle_name" />
              </div>
              <div class="form-group col-md-4">
                <label for="">Last Name</label>
                <input type="text" class="form-control" v-model="last_name" />
              </div>
            </div>
            <div class="row mb-4">
              <div class="form-group col-md-4">
                        <label for="inputCity">Role</label>
                        <select id="" v-model="role" class="form-control">
                            <option v-for="(crole,index) in roles" :key="index" :value="crole.id" class="text-capitalize">{{crole.role}}</option>
                        </select>
                </div>

              <div class="form-group col-md-4">
                <label for="inputCity">Phone</label>
                <input type="text" class="form-control" v-model="phone" />
              </div>
              <div class="form-group col-md-4">
                <label for="inputState">Gender</label>
                <select id="inputState" v-model="gender" class="form-control">
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
            </div>

            <div class="mb-4">
                <div class="form-group">
                    <label for="inputZip">Date Of Birth</label>
                    <input type="date" class="form-control" v-model="birth_date" />
                </div>
            </div>

            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button type="submit" class="btn cbtn">Create User</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import {Modal} from 'bootstrap';

export default {
  setup() {
    const store = useStore();
    const username = ref();
    const email = ref();
    const gender = ref();
    const birth_date = ref();
    const phone = ref();
    const first_name = ref();
    const middle_name = ref();
    const last_name = ref();
    const role = ref();
    const sBranch = ref();
    const roles = ref();
    let addUserModal;


    onMounted(()=>{
        addUserModal = new Modal('#addUser',{keyboard:false})
    })




    const createUser = () => {
      let body = {
        username: username.value,
        email: email.value,
        birth_date: birth_date.value,
        phone: phone.value,
        first_name: first_name.value,
        middle_name: middle_name.value,
        last_name: last_name.value,
        gender: gender.value,
        branch_id: 1,
        role:role.value
       // access_routes: JSON.stringify(accR.value),
      };



      store.dispatch("registerUser", body ).then(() => {
        $("#addUser").modal("hide");
        username.value = "";
        email.value = "";
        birth_date.value = "";
        phone.value = "";
        first_name.value = "";
        middle_name.value = 0;
        last_name.value = "";
        gender.value = "";
        sBranch.value = "";
        role.value = ""
      });
      addUserModal.hide();

      setTimeout(store.dispatch("fetchAllUsers"),2000)
    };

    //getRoles
    store.dispatch("getRoles");

    watch(
      () => [...store.getters.roles],
      (newRoles) => {
        roles.value = newRoles;
      }
    );

    return {
      username,
      email,
      gender,
      birth_date,
      phone,
      first_name,
      middle_name,
      last_name,
      role,
      createUser,
      roles
    };
  },
};
</script>
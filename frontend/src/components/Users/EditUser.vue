<template>
  <div class="modal fade" id="editUser" tabindex="-1" aria-labelledby="editUserLabel" aria-hidden="true">
  <div class="modal-dialog modal-xl">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="editUserLabel">Edit User</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
            <div class="row">
                <div class="col-md-12 px-3">
                <form @submit.prevent="">
                    <div class="row mb-3">
                    <div class="form-group col-md-6">
                        <label>Email</label>
                        <input type="email" class="form-control" v-model="email" disabled />
                    </div>
                    <div class="form-group col-md-6">
                        <label for="">Username</label>
                        <input
                        type="text"
                        class="form-control"
                        v-model="username"
                        disabled
                        />
                    </div>
                    </div>
                    <div class="row mb-3">
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
                        <option
                            v-for="(crole, index) in roles"
                            :key="index"
                            :value="crole.id"
                            class="text-capitalize"
                        >
                            {{ crole.role }}
                        </option>
                        </select>
                    </div>
                    <div class="form-group col-md-4">
                        <label for="inputState">Gender</label>
                        <select id="inputState" v-model="gender" class="form-control">
                        <option :value="user.gender" class="d-none" selected>
                            {{ user.gender }}
                        </option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        </select>
                    </div>
                    <div class="form-group col-md-4">
                        <label for="inputZip">Date Of Birth</label>
                        <input type="date" class="form-control" v-model="birth_date" />
                    </div>
                    </div>
                    <div class="form-row">
                    <div class="col">
                        <label for="">Phone Number</label>
                        <input type="text" class="form-control" v-model="phone" />
                    </div>
                    </div>


                    <div class="mt-3">
                                        <div class="">
                <p class="card-title">Activity</p>
                <div class="card">
                    <div class="card-body d-flex justify-content-between">
                    <div class="">
                        <small class="card-subtitle  text-muted">Last Login</small>
                        <p class="card-text" v-if="user.last_login !== null">
                        {{ new Date(user.last_login).toDateString() }}
                        </p>
                        <p class="card-text" v-else>Unknown</p>
                    </div>

                    <div class="">
                        <small class="card-subtitle text-muted">Created At</small>
                        <p class="card-text">
                        {{ new Date(user.created_at).toDateString() }}
                        </p>
                    </div>

                    <div class="">
                        <small class="card-subtitle text-muted">Is Active</small>
                        <p class="card-text">{{ user.is_active }}</p>
                    </div>

                    <div>
                    <!--
                        <button
                        class="btn btn-sm btn-block cbtn"
                        data-toggle="modal"
                        data-target="#userActivity"
                        @click="getUserActivity(user.id)"
                        >
                        <small>More Details <i class="uil uil-arrow-up-right"></i></small>
                        </button>
                    -->  
                    </div>
                    </div>
                </div>
                </div>
                    </div>


                    <div class="form-group row mt-4">
                    <div class="col">
                        <button
                        type="submit"
                        class="btn cbtn cbtn-alt btn-block"
                        @click="updateUser()"
                        >
                        <i class="bi bi-arrow-bar-up"></i> Update User
                        </button>
                    </div>
                    <div class="col">
                        <button class="btn btn-light btn-block" @click="resetPass()">
                        <i class="uil uil-history-alt"></i>Reset Password
                        </button>
                    </div>

                    <div class="col">
                        <button @click="deleteUser(user.id)" class="btn btn-secondary btn-block">
                        <i class="uil uil-trash-alt"></i> Delete Account
                        </button>
                    </div>
                    </div>
                </form>
                </div>

  </div>
      </div>

    </div>
  </div>
</div>
 
</template>
<script>
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { ref, watch,toRefs,onMounted} from "vue";
import {Modal} from 'bootstrap';

export default {
  props:{
    user:Object
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    const roles = ref(store.getters.roles);
    const {user} = toRefs(props)

    const username = ref();
    const password = ref();
    const email = ref();
    const gender = ref();
    const birth_date = ref();
    const phone = ref();
    const first_name = ref();
    const middle_name = ref();
    const last_name = ref();
    const role = ref();
    let editUser;

    onMounted(()=>{editUser=new Modal('#editUser',{keyboard:false})});

    watch(()=>user.value,(newUser)=>{
            console.log(newUser)
            if(newUser){
                username.value = user.value.username;
                password.value = ''
                email.value = user.value.email;
                gender.value =user.value.gender;
                birth_date.value = user.value.birth_date;
                phone.value = user.value.phone;
                first_name.value = user.value.first_name;
                middle_name.value = user.value.middle_name;
                last_name.value = user.value.last_name;
                role.value =user.value.role;
            }
    })




    store.dispatch("getRoles");

    watch(
      () => [...store.getters.roles],
      (newRoles) => {
        roles.value = newRoles;
      }
    );

    const resetPass = () => {
      store
        .dispatch("resetUserPass",
           user.value.email,
        )
        .then(() => {});
    };

    const updateUser = () => {
      let newDetails = {
        username: username.value,
        email: email.value,
        gender: gender.value,
        birth_date: birth_date.value,
        phone: phone.value,
        first_name: first_name.value,
        middle_name: middle_name.value,
        last_name: last_name.value,
        role: role.value,
        branch_id: 1,
      };

      store.dispatch("updateUser", {
        id: user.value.id,
        user:newDetails
      });
      editUser.hide();
      store.dispatch("fetchAllUsers");
    };


 


    const deleteUser = (id) => {
      Swal.fire({
        title: "Do you want to Delete this User?",
        showCancelButton: true,
        confirmButtonText: "Proceed",
      }).then((result) => {
        if (result.isConfirmed) {
          store
            .dispatch("deleteUser", { id, token: getToken() })
            .then(() => {
              router.push({name:"Users"})
            });
        }
      });
    };

    return {
      user,
      username,
      password,
      email,
      gender,
      birth_date,
      phone,
      first_name,
      middle_name,
      last_name,
      role,
      resetPass,
      updateUser,
      roles,
      deleteUser
    };
  },
};
</script>
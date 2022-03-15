<template>
  <div class="row">
    <div class="col-md-6">
      <div class="card shadow mb-4">
        <form @submit.prevent="updateBasic">
          <div class="card-body">
            <div class="form-group">
              <label for="">Product Name</label>
              <input type="text" v-model="product.title" placeholder="Product Name" class="form-control">
            </div>
            <div class="form-group">
              <label for="">Product SKU</label>
              <input type="text" v-model="product.sku" placeholder="Product Name" class="form-control">
            </div>
            <div class="form-group">
              <label for="">Description</label>
              <textarea v-model="product.description" id="" cols="30" rows="4" class="form-control"></textarea>
            </div>
          </div>
          <button type="submit" class="btn btn-google text-center w-100">Update</button>
        </form>
      </div>
      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">Media</h6>
        </div>
        <div class="card-body border">
          <vue-dropzone ref="myVueDropzone" v-on:vdropzone-success="changeImage()" id="dropzone"
                        :options="dropzoneOptions"></vue-dropzone>
        </div>
      </div>
      <!--        <div class="card shadow mb-4">-->
      <!--          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">-->
      <!--            <h6 class="m-0 font-weight-bold text-primary">Media</h6>-->
      <!--          </div>-->
      <!--          <div class="card-body border">-->
      <!--            <vue-dropzone ref="myVueDropzone" id="dropzone"-->
      <!--                          :options="dropzoneOptions"></vue-dropzone>-->
      <!--          </div>-->
      <!--        </div>-->
    </div>
    <div class="col-md-6">
      <div class="card mb-3 px-3 py-4">
        <p class="card-title text-primary">Variations list</p>
        <div>
          <table class="table table-hover">
            <tr>
              <th>Variation</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Action</th>
            </tr>
            <tr v-for="(variation,index) in product.get_product_variation_prices">
              <td>
                <!--                <span>{{ variation.product_variant_one.variant_title}}</span>-->
                <span
                    v-if="variation.product_variant_one !== null">{{
                    variation.product_variant_one.variant_title
                  }} / </span>
                <span
                    v-if="variation.product_variant_two !== null">{{
                    variation.product_variant_two.variant_title
                  }} / </span>
                <span
                    v-if="variation.product_variant_three !== null">{{
                    variation.product_variant_three.variant_title
                  }} / </span>

              </td>
              <td>{{ variation.price }}</td>
              <td>{{ variation.stock }}</td>
              <td style="cursor: pointer" @click.prevent="deleteVariant(variation.id,index)">Delete</td>
            </tr>
          </table>
        </div>
      </div>

      <form @submit.prevent="addMoreVariant">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Variants</h6>
          </div>
          <div class="card-body">
            <div class="row" v-for="(item,index) in product_variant">
              <div class="col-md-4">
                <div class="form-group">
                  <label for="">Option</label>
                  <select v-model="item.option" class="form-control">
                    <option v-for="variant in variants"
                            :value="variant.id">
                      {{ variant.title }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="col-md-8">
                <div class="form-group">
                  <label v-if="product_variant.length != 1" @click="product_variant.splice(index,1); checkVariant"
                         class="float-right text-primary"
                         style="cursor: pointer;">Remove</label>
                  <label v-else for="">.</label>
                  <input-tag v-model="item.tags" @input="checkVariant" class="form-control"></input-tag>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer" v-if="product_variant.length < variants.length && product_variant.length < 3">
            <button @click="newVariant" class="btn btn-primary">Add another option</button>
          </div>

          <div class="card-header text-uppercase">Preview</div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                <tr>
                  <td>Variant</td>
                  <td>Price</td>
                  <td>Stock</td>
                </tr>
                </thead>
                <tbody>
                <tr v-for="variant_price in product_variant_prices">
                  <td>{{ variant_price.title }}</td>
                  <td>
                    <input type="text" class="form-control" v-model="variant_price.price">
                  </td>
                  <td>
                    <input type="text" class="form-control" v-model="variant_price.stock">
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <button class="btn btn-google w-100" style="cursor: pointer" type="submit">Add more variants</button>
      </form>

    </div>
  </div>
</template>

<script>
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
import InputTag from 'vue-input-tag'

export default {
  components: {
    vueDropzone: vue2Dropzone, InputTag
  },
  data() {
    return {
      product: {},
      product_variant: [
        {
          option: this.variants[0].id,
          tags: []
        }
      ],
      product_variant_prices: [],
      dropzoneOptions: {
        url: `/product/api/add/image/${this.id}/`,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: {
          "X-CSRFToken": this.getCookie('csrftoken')
        }
      }
    }
  },
  props: ['id', 'variants'],
  mounted() {
    this.get_product();
  },
  methods: {
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    deleteVariant(variationID, index) {
      if (confirm("Do you want to delete?")){
        let config = {
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
        }
      }
      this.$http.delete(`/product/api/remove/variation/${variationID}/`, config)
          .then(() => {
            this.$delete(this.product.get_product_variation_prices,index)
            // this.product.get_product_variation_prices.splice()
          })
      }
    },
    addMoreVariant() {
      let formdata = new FormData()
      formdata.append("product_variant_prices", JSON.stringify(this.product_variant_prices))
      formdata.append("product_variant", JSON.stringify(this.product_variant))
      let config = {
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
        }
      }
      this.$http.post(`/product/api/add/variation/${this.id}/`, formdata, config)
      .then(res =>  {
        this.product.get_product_variation_prices = res.data
      })
    },
    newVariant() {
      let all_variants = this.variants.map(el => el.id)
      let selected_variants = this.product_variant.map(el => el.option);
      let available_variants = all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 === entry2))
      // console.log(available_variants)

      this.product_variant.push({
        option: available_variants[0],
        tags: []
      })
    },

    // check the variant and render all the combination
    checkVariant() {
      let tags = [];
      this.product_variant_prices = [];
      this.product_variant.filter((item) => {
        tags.push(item.tags);
      })

      this.getCombn(tags).forEach(item => {
        this.product_variant_prices.push({
          title: item,
          price: 0,
          stock: 0
        })
      })
    },

    // combination algorithm
    getCombn(arr, pre) {
      pre = pre || '';
      if (!arr.length) {
        return pre;
      }
      let self = this;
      let ans = arr[0].reduce(function (ans, value) {
        return ans.concat(self.getCombn(arr.slice(1), pre + value + '/'));
      }, []);
      return ans;
    },
    get_product() {
      this.$http.get(`/product/api/product/edit/${this.id}/`)
          .then(res => {
            this.product = res.data
          })
    },
    updateBasic() {
      let config = {
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
        }
      }
      this.$http.put(`/product/api/product/update/basic/${this.id}/`, {
        title: this.product.title,
        sku: this.product.sku,
        description: this.product.description,
      }, config)
          .catch(err => {
            console.log(err.response.data)
          })
    }
  },
}
</script>

<style scoped>

</style>
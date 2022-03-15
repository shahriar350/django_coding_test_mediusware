<template>
  <div>
    <div>

      <div class="card">
        <form @submit.prevent="searchBar" class="card-header">
          <div class="form-row justify-content-between">
            <div class="col-md-2">
              <input v-model="search.title" type="text" name="title" placeholder="Product Title" class="form-control">
            </div>
            <div class="col-md-2">
              <select v-model="search.variant" name="variant" id="" class="form-control">
                <option selected disabled>--Select A Variant--</option>
                <option :value="variant.id" v-for="(variant,index) in variants" :key="index">
                  {{ variant.title }}
                </option>
              </select>
            </div>

            <div class="col-md-3">
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">Price Range</span>
                </div>
                <input type="text" name="price_from" v-model="search.price_start" aria-label="First name"
                       placeholder="From"
                       class="form-control">
                <input type="text" name="price_to" v-model="search.price_end" aria-label="Last name" placeholder="To"
                       class="form-control">
              </div>
            </div>
            <div class="col-md-2">
              <input type="date" v-model="search.created_date" name="date" placeholder="Date" class="form-control">
            </div>
            <div class="col-md-1">
              <button type="submit" class="btn btn-primary float-right"><i class="fa fa-search"></i></button>
            </div>
          </div>
        </form>

        <div class="card-body">
          <div class="table-response">
            <table class="table">
              <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Description</th>
                <th>Variant</th>
                <th width="150px">Action</th>
              </tr>
              </thead>

              <tbody>
              <tr v-for="(product,index) in products.results" :key="index">
                <td>{{ (products.page_size * products.current_page_number - 1) + index }}</td>
                <td>{{ product.title }} <br> Created at :
                  {{ new Date(product.created_at).toUTCString() | moment("from", "now", true) }} ago
                </td>
                <td>{{ product.description }}</td>
                <td>
                  <span v-for="(price,priceIndex) in product.get_product_variation_prices" :key="priceIndex">
                    <dl
                        class="row mb-0" style="height: 80px; overflow: hidden" id="variant">
                    <dt class="col-sm-3 pb-0">
                      <span
                          v-if="price.product_variant_one !== null">{{
                          price.product_variant_one.variant_title
                        }} / </span>
                      <span
                          v-if="price.product_variant_two !== null">{{
                          price.product_variant_two.variant_title
                        }} / </span>
                      <span
                          v-if="price.product_variant_three !== null">{{
                          price.product_variant_three.variant_title
                        }}</span>
                      <!--                      <span>{{prices.product_variant_two.variant.title}}</span>-->
                      <!--                      <span v-if="Object.keys(price.product_variant_three).length > 0">{{price.product_variant_three.variant.title}}</span>-->
                      <!--                      XL/ Black/ Full-->
                    </dt>
                    <dd class="col-sm-9">
                      <dl class="row mb-0">
                        <dd class="col-sm-4 pb-0">Price : {{ price.price }}</dd>
                        <dd class="col-sm-8 pb-0">InStock : {{ price.stock }}.</dd>
                      </dl>
                    </dd>
                  </dl>
                  </span>

                  <button onclick="$('#variant').toggleClass('h-auto')" class="btn btn-sm btn-link">Show more
                  </button>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <a :href="`/product/edit/${product.id}/`" class="btn btn-success">Edit</a>
                  </div>
                </td>
              </tr>

              </tbody>

            </table>
          </div>

        </div>

        <div class="card-footer">
          <div class="row justify-content-between">
            <div class="col-md-6">
              <p>Showing {{ products.page_size * products.current_page_number - 1 }} to
                {{ products.page_size * products.current_page_number }} out of {{ products.total_objects }}</p>
            </div>
            <div class="col-md-2">
              <nav aria-label="Page navigation example">
                <ul class="pagination">
                  <li class="page-item">
                    <a class="page-link" @click="get_product_list(1)" aria-label="Previous">
                      <span aria-hidden="true">&laquo;</span>
                    </a>
                  </li>
                  <li v-for="(pages,pageIndex) in products.total_pages" :key="pageIndex" class="page-item"
                      style="cursor: pointer"><a
                      class="page-link" @click="get_product_list(pageIndex + 1)">{{ pageIndex + 1 }}</a></li>
                  <li class="page-item">
                    <a class="page-link" @click="get_product_list(products.total_pages)" aria-label="Next">
                      <span aria-hidden="true">&raquo;</span>
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  data() {
    return {
      products: [],
      variants: [],
      search: {
        title: '',
        variant: '',
        price_start: '',
        price_end: '',
        created_date: '',
      }
    }
  },

  created() {
    this.get_product_list();
    this.get_variant_list();
    this.getCookie('csrftoken');
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
    searchBar() {
      // this.$http.post("/product/api/product/search/", this.search)
      this.$http.get(`/product/api/product/search/?title=${this.search.title}&variant=${this.search.variant}&price_start=${this.search.price_start}&price_end=${this.search.price_end}&created_date=${this.search.created_date}`)
          .then(res => {
            this.products = res.data
          })

    },
    get_variant_list() {
      this.$http.get('/product/api/variant/list/')
          .then(res => {
            this.variants = res.data
          })
    },
    get_product_list(id) {
      if (id === undefined) {
        id = 1
      }
      this.$http.get(`/product/api/list?page=${id}`)
          .then(res => {
            this.products = res.data
          })
    }
  },
}
</script>

<style scoped>

</style>
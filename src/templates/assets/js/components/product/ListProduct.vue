<template>
  <div>
    <div>

      <div class="card">
        <form action="" method="get" class="card-header">
          <div class="form-row justify-content-between">
            <div class="col-md-2">
              <input type="text" name="title" placeholder="Product Title" class="form-control">
            </div>
            <div class="col-md-2">
              <select name="variant" id="" class="form-control">
                <option selected disabled>--Select A Variant--</option>

              </select>
            </div>

            <div class="col-md-3">
              <div class="input-group">
                <div class="input-group-prepend">
                  <span class="input-group-text">Price Range</span>
                </div>
                <input type="text" name="price_from" aria-label="First name" placeholder="From"
                       class="form-control">
                <input type="text" name="price_to" aria-label="Last name" placeholder="To" class="form-control">
              </div>
            </div>
            <div class="col-md-2">
              <input type="date" name="date" placeholder="Date" class="form-control">
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
                    <a href="" class="btn btn-success">Edit</a>
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
    }
  },

  created() {
    this.get_product_list();
  },
  methods: {
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
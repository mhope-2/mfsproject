import axios from "axios";
import endPoint
 from "../config/config";
export const search = (query, arr) => {
  const results = arr.filter((item) => {
    if (JSON.stringify(item).toLowerCase().includes(query.toLowerCase())) {
      return item;
    }
  });
  return results;
};

export const searchProduct = (query, arr) => {
  let searchedProduct = [];
  let products = [];
  if (query !== "") {
    arr.forEach((product) => {
      if (product.name.toLowerCase().includes(query.toLowerCase())) {
        return searchedProduct.push(product);
      }
    });
  }

  return searchedProduct;
};

export const searchPicklist = (query, arr) => {
  let data = [];
  arr.map((inv) => {
    if (inv.pick_status === query) {
      data.push(inv);
    }
  });

  return data;
};

export const searchInvoice = (query, arr) => {
  let data = [];
  for (var x = 0; x < arr?.length; x++) {
    if (
      arr[x].partial_payment === query &&
      arr[x].refund_status !== "Refunded"
    ) {
      data.push(arr[x]);
    }
  }
  return data;
};
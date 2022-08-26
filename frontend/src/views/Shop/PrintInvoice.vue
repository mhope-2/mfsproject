<template>
  <div v-if="sInvoice">
    <div style="height:100vh; align-items:center; justify-content:center" class="d-flex">
      <div class="text-center blob">
        <h1><i class="uil uil-print"></i></h1>
        Generating PDF .....
      </div>
    </div>
  </div>
</template>

<script>
import {ref,watch} from 'vue';
import {useRoute,useRouter} from 'vue-router';
import QRcode from "qrcode";
import {useStore} from 'vuex';
import pdfMake from 'pdfmake'
export default {
    setup() {
        const router = useRouter();
        var uniFied = new Intl.NumberFormat('en-gh',{
            style: 'currency',
            currency: 'GHS',
        });
        const store = useStore();
        const sInvoice = ref(store.getters.getToPrint);
        const qrUrl = ref();
        const sub_total = ref();
        const br_address = ref();
        let filterPayOpts =[];
        const refunded = ref([]);
      
        
        if(!sInvoice.value.invoice){
          router.push({name:'invoices'})
        }

      var productsTable =(sInvoice.value.invoice.issued_by == "Refunded")?[[{text:"Item",border:[1,0,1,1],bold: true},{text:"Price",border:[1,0,1,1],bold: true}, {text:"Quantity",border:[1,0,1,1],bold: true,alignment:'right'}, {text:"Refund Quantity",border:[1,0,1,1],bold: true,alignment:'center'},{text:"Line Total",border:[1,0,1,1],bold: true,alignment:'right'}]]:[[{text:"Item",border:[1,0,1,1],bold: true},{text:"Price",border:[1,0,1,1],bold: true}, {text:"Quantity",border:[1,0,1,1],bold: true,alignment:'right'}, {text:"Line Total",border:[1,0,1,1],bold: true,alignment:'right'}]];
        //PDF Generator
         const generatePDF = () => {     
            var dd = {
  content: [
    { text: "mfs project", style: "header", alignment: "center"},
    {
      columns: [
        { text: "" },
        {
          text: 'Vancouver, Makola',
          fontSize: 7,
          alignment: "center",
        },
        { text: "" },
      ],
      margin: [0,0,4,10],
    },
        {
      columns: [
        {columns:[
           { text: `Invoice No.:`, bold:true},
           {text:` ${sInvoice.value.invoice.invoice_no} ${(sInvoice.value.invoice.issued_by == "Refunded")?"(R)":""}`}
        ]},
        { text: "" },
        {columns:[
          {text:`Date:`,bold:true},
          { text: `${new Date(sInvoice.value.invoice.date_paid||sInvoice.value.invoice.created_at).toLocaleDateString()}`, alignment: "right" },
        ]}
        
      ],
      margin: [0, 10, 0, 0],
    },
        {
      columns: [
        { columns:[
          {text:`Customer: `, bold:true},
          {text: `${sInvoice.value.invoice.customer_first_name} ${sInvoice.value.invoice.customer_last_name||""}`}
        ] },
        { text: "" },

       {
         columns:[
           {text:`Sales Person:`,bold:true},
           {text:`${sInvoice.value.invoice.issued_by}`,alignment:'right'}
         ]
        }
        
      ],
      margin: [0, 10, 0, 30],
    },  



    {
      style: "",
      table: {
        body:productsTable,
        widths:(sInvoice.value.invoice.issued_by == "Refunded")?['*',40,44,50,50]:['*',44,50,50],
        alignment:'center'
      },
      layout:{
                hLineColor: function (i, node) {
                  return (i === 0 || i === node.table.body.length) ? '#eee' : '#eee';
                },
                vLineColor: function (i, node) {
                  return (i === 0 || i === node.table.widths.length) ? '#fff' : '#fff';
                },
                paddingLeft: function(i, node) { return 4; },
                paddingRight: function(i, node) { return 4; },
                paddingTop: function(i, node) { return 10; },
                paddingBottom: function(i, node) { return 10; }
          },
    },
    {text:'',margin:[0,30,0,30]},
    {
      columns:[
              {table:{
          body: filterPayOpts,
          widths:[100,'*'],
        },
        
        layout:{
                        hLineColor: function (i, node) {
                          return (i === 0 || i === node.table.body.length) ? '#eee' : '#eee';
                        },
                        vLineColor: function (i, node) {
                          return (i === 0 || i === node.table.widths.length) ? '#fff' : '#fff';
                        },
                                        paddingLeft: function(i, node) { return 4; },
                        paddingRight: function(i, node) { return 4; },
                        paddingTop: function(i, node) { return 6; },
                        paddingBottom: function(i, node) { return 6; }
         },
        },  
        {table:{
          body: [
            [{text:'Sub Total',border:[1,0,1,1],   bold: true,}, {text:` ${uniFied.format(parseFloat(sub_total.value.toFixed(2)))}`,alignment:'right',border:[1,0,1,1]}],
            [{text:'Discount:',bold:true}, {text:` ${uniFied.format(parseFloat(sub_total.value)-parseFloat(sInvoice.value.invoice.net_total))}`,alignment:'right'}],
            [{text:`GetFund:`,bold:true},{text:uniFied.format(parseFloat(sInvoice.value.invoice.get_fund_value||0)),alignment:'right'}],
            [{text:`NHIL:`,bold:true},{text:uniFied.format(parseFloat(sInvoice.value.invoice.nhil_value)),alignment:'right'}],
            [{text:`COVID Levy:`,bold:true},{text:uniFied.format(parseFloat(sInvoice.value.invoice.covid_levy_value)),alignment:'right'}],
            [{text:`VAT: `,bold:true},{text:uniFied.format(parseFloat(sInvoice.value.invoice.vat_value)),alignment:'right'}],
            [{text:'Amount Due',bold:true}, {text:`  ${uniFied.format(parseFloat(sInvoice.value.invoice.net_total))}`,alignment:'right'}],
          ],
          widths:[100,'*'],
        },
        
         layout:{
                hLineColor: function (i, node) {
                  return (i === 0 || i === node.table.body.length) ? '#eee' : '#eee';
                },
                vLineColor: function (i, node) {
                  return (i === 0 || i === node.table.widths.length) ? '#fff' : '#fff';
                },
                                paddingLeft: function(i, node) { return 4; },
                paddingRight: function(i, node) { return 4; },
                paddingTop: function(i, node) { return 6; },
                paddingBottom: function(i, node) { return 6; }
          },
        },
  

      ]
    },
    {image:qrUrl.value,
      width:50,
      alignment:'right'
      ,margin:[0,30,0,0]
    }

  ],
  
  footer:{
    columns:[
      {text:'THANK YOU FOR SHOPPING WITH US',alignment:'center',color:'#03C199',margin:[0,10,0,0]},
      
    ]
  },

  styles: {
    header: {
      fontSize: 16,
      bold: true,
      margin: [0, 0, 0, 10],
    },
    subheader: {
      fontSize: 14,
      bold: true,
      margin: [0, 10, 0, 5],
    },
    tableEx: {
      
    },
    tableHeader: {
      bold: true,
      fontSize: 14,
      color: "black",
    },
  },
  defaultStyle: {
    font:'Readex',
       fontSize: 9,
  },
}   

            //Add Custom Fonts
          pdfMake.fonts = {
              Readex:{
                normal:'https://res.cloudinary.com/dan6ksd6d/raw/upload/v1645005859/ReadexPro-VariableFont_wght_fhpenp.ttf',
                bold:'https://res.cloudinary.com/dan6ksd6d/raw/upload/v1646551496/FontsFree-Net-ReadexPro-bold_yxtkf9.ttf',
                italics:'https://res.cloudinary.com/dan6ksd6d/raw/upload/v1645005859/ReadexPro-VariableFont_wght_fhpenp.ttf',
                boldItalics:'https://res.cloudinary.com/dan6ksd6d/raw/upload/v1645005859/ReadexPro-VariableFont_wght_fhpenp.ttf',
              }
            }          
     
            pdfMake.createPdf(dd).open();
        }
    
    if(sInvoice.value.invoice){
      QRcode.toDataURL(JSON.stringify(sInvoice.value.invoice.invoice_no + sInvoice.value.invoice.customer_phone + sInvoice.value.invoice.createdAt) + "u" + sInvoice.value.invoice.customer_phone).then((url) => {
         qrUrl.value = url;
       });


      sInvoice.value.invoice_items.forEach((item,index)=>{
          let itemArr =(sInvoice.value.invoice.issued_by == "Refunded")?[item.product_details.product_description,item.unit_price,{text:item.quantity,alignment:`center`},{text:(parseInt(item.quantity)*parseFloat(item.refunded_amount))/(parseInt(item.quantity)*parseFloat(item.unit_price)) || 0,alignment:`center`},{text:parseInt(item.quantity)*parseFloat(item.unit_price),alignment:'center'}]:[item.product_details.product_description,item.unit_price,{text:item.quantity,alignment:`center`},{text:parseInt(item.quantity)*parseFloat(item.unit_price),alignment:'center'}];
          productsTable.push(itemArr);
          if(item.refund_status = "Refunded"){
            refunded.value.push(item);
          }
        })
        
        let paymentOpts = [];
        const {cash,mobile_money,bank_transfer,credit_line} = sInvoice.value.invoice;
        paymentOpts = [cash,mobile_money,bank_transfer,credit_line];


        paymentOpts.forEach((item,index)=>{
            if(parseFloat(item)>0 || parseFloat(item)<0){
                if(index == 0){
                  filterPayOpts.push([{text:`Cash:`,border:[1,0,1,1],bold: true},{text:` ${uniFied.format(parseFloat(item).toFixed(2))}`,border:[1,0,1,1]}]);
                }
                else if(index == 1){
                       filterPayOpts.push([{text:`Momo:`,border:[1,0,1,1],bold: true},{text:`${uniFied.format(parseFloat(item).toFixed(2))}`}]);
                }
                else if(index == 2){
                       filterPayOpts.push ([{text:`Bank Transfer:`,border:[1,0,1,1],bold: true},{text:` ${uniFied.format(parseFloat(item).toFixed(2))}`,border:[1,0,1,1]}]);
                }
                else if(index == 3){
                       filterPayOpts.push([{text:`Credit:`,border:[1,0,1,1],bold: true},{text:`${uniFied.format(parseFloat(item).toFixed(2))}`,border:[1,0,1,1]}]);
                }
            }
        })
        filterPayOpts.push([{text:`Balance:`,border:[1,0,1,1],bold: true},{text:` ${uniFied.format(parseFloat(sInvoice.value.invoice.change).toFixed(2))}`,border:[1,0,1,1]}]);
        filterPayOpts.push([{text:`Amount Received:`,border:[1,0,1,1],bold: true},{text:` ${uniFied.format(parseFloat(sInvoice.value.invoice.amount_received).toFixed(2))}`,border:[1,0,1,1]}]);
        if(sInvoice.value.invoice.issued_by == "Refunded"){
          filterPayOpts.push([{text:`Refund Amount:`,border:[1,0,1,1],bold: true},{text:` ${uniFied.format(sInvoice.value.invoice_items.reduce((a,b)=>{
            return parseFloat(a)+parseFloat(b.refunded_amount||0)},0))}`,border:[1,0,1,1]}]);
        }

    let sub_arr = [];
    sInvoice.value.invoice_items.forEach(item=>{
        const lineTotal = parseFloat(item.quantity )*parseFloat(item.product_details.unit_price);
        sub_arr.push(lineTotal);
    });

    sub_total.value = sub_arr.reduce((a,b)=>a+b,0);
    }



    watch(()=>store.getters.getToPrint,(newInvoice)=>{
        sInvoice.value = newInvoice;
    })


    const completPDF = () =>{
      generatePDF();
      router.push({name:'invoices'})
    }
        setTimeout(completPDF, 2000);

        return {generatePDF,sInvoice,qrUrl,sub_total}
    },
}
</script>

  <style scoped>
    .blob {
    transform: scale(1);
    animation: pulse-black 2s infinite;
    color: #03C199 !important;
  }

  @keyframes pulse-black {
    0% {
      transform: scale(0.95);
      opacity: 1;
    }
    
    70% {
      transform: scale(1);
      opacity: 0;
    }
    
    100% {
      transform: scale(0.95);
       opacity: 1;
    }
  }
</style>
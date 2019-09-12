odoo.define('pos_product_quantity.p_quantity', function (require) {
"use strict";

    var gui = require('point_of_sale.gui');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;

    var QuantitiesPopup = PopupWidget.extend({
	    template: 'QuantitiesPopup',
	    show: function(options){
	        var self = this;
	        this._super(options);
	        if (options.order_line){
	            var product_id = options.order_line.product.id
	            var location_id = options.location_id
                rpc.query({
                    model: 'pos.product.qty',
                    method: 'get_quantities',
                    args: [[], product_id,location_id],
                }).then(function (data) {
                    if (data) {
                        for (var warehouse in data.warehouses) {
                            var  warehouse_data = data.warehouses[warehouse]
                            $("#myTable").find('tbody').append($('<tr><td>'+warehouse_data.name+'</td><td>'+warehouse_data.quantity+'</td></tr>').addClass(function(){
                                if (warehouse_data.my_company){
                                    return 'myClass';
                                }else{
                                    return '';
                                }
                            }));
                        };

                        $('.total-qty').text(data.total_qty);
                    } else {
                        alert(_t("Please Select Product"));
                    }
                }).fail(function () {
                    alert(_t("Please Select Product"));
                });

                this.renderElement();
                }else{
                    alert("Please select the product ");
                }
	    },
	    renderElement: function() {
            var self = this;
            this._super();
    	},

	});

	gui.define_popup({name:'quantities_popup', widget: QuantitiesPopup});

    var ProductQuantity = screens.ActionButtonWidget.extend({
        template: 'ProductQuantity',
        button_click: function(){
            var order = this.pos.get_order();
            var selected_line = order.get_selected_orderline();
            var location_id = this.pos.config.stock_location_id[0]
            if (selected_line) {
                	this.gui.show_popup('quantities_popup',{'order_line':selected_line,'location_id':location_id});
            }else {
                alert(_t("Please select the product !"));
            }

        },

    });

    screens.define_action_button({
        'name': 'product_quantity',
        'widget': ProductQuantity,
        'condition': function(){
            return this.pos.config.display_product_qty;
        },
    });

});


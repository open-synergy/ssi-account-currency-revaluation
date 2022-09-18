# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

{
    "name": "Currency Revaluation",
    "version": "14.0.1.2.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_financial_accounting",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "configuration_helper",
        "ssi_duration_mixin",
        "currency_rate_inverted",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        "data/account_journal_data.xml",
        "views/res_config_settings_views.xml",
        "views/account_currency_revaluation_views.xml",
    ],
    "demo": [
        "demo/account_account_demo.xml",
        "demo/account_journal_demo.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}

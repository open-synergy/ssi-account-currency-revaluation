# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class AccountCurrencyRevaluation(models.Model):
    _name = "account.currency_revaluation"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Currency Revaluation"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = True
    _automatically_insert_done_button = True

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    currency_id = fields.Many2one(
        string="Account Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )
    account_id = fields.Many2one(
        string="Account to Revaluate",
        comodel_name="account.account",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    gain_account_id = fields.Many2one(
        string="Unrealized Gain Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    loss_account_id = fields.Many2one(
        string="Unrealized Loss Account",
        comodel_name="account.account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="Accounting Entry",
        comodel_name="account.move",
        ondelete="restrict",
        readonly=True,
    )

    @api.depends(
        "date",
        "account_id",
        "currency_id",
        "company_id",
    )
    def _compute_amount(self):
        MoveLine = self.env["account.move.line"]
        Currency = self.env["res.currency"]
        for record in self:
            amount_in_company_currency = (
                amount_in_account_currency
            ) = rate_at_revaluation = amount_revaluation = amount_diff = 0.0
            rate_quotation = "indirect"

            criteria = [
                ("account_id", "=", record.account_id.id),
                ("date", "<=", record.date),
            ]
            if (
                record.account_id
                and record.date
                and record.currency_id
                and record.company_currency_id
            ):
                compute_result = MoveLine.read_group(
                    criteria,
                    fields=["balance", "amount_currency"],
                    groupby=["account_id"],
                    lazy=False,
                )[0]
                amount_in_company_currency = compute_result["balance"]
                amount_in_account_currency = compute_result["amount_currency"]

                rate_at_revaluation = Currency._get_conversion_rate(
                    record.currency_id,
                    record.company_currency_id,
                    record.company_id,
                    record.date,
                )
                amount_revaluation = record.currency_id._convert(
                    amount_in_account_currency,
                    record.company_currency_id,
                    record.company_id,
                    record.date,
                )
                amount_diff = amount_in_company_currency - amount_revaluation

            record.amount_in_company_currency = amount_in_company_currency
            record.amount_in_account_currency = amount_in_account_currency
            record.rate_at_revaluation = rate_at_revaluation
            record.amount_revaluation = amount_revaluation
            record.rate_quotation = rate_quotation
            record.amount_diff = amount_diff

    amount_in_company_currency = fields.Monetary(
        string="Amount in Company Currency",
        compute="_compute_amount",
        currency_field="company_currency_id",
        store=True,
        compute_sudo=True,
    )
    amount_in_account_currency = fields.Monetary(
        string="Amount in Account Currency",
        compute="_compute_amount",
        currency_field="currency_id",
        store=True,
        compute_sudo=True,
    )
    rate_at_revaluation = fields.Float(
        string="Revaluation Rate",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
    )
    rate_quotation = fields.Selection(
        string="Rate Quotation",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        selection=[
            ("direct", "Direct"),
            ("indirect", "Indirect"),
        ],
    )
    amount_revaluation = fields.Monetary(
        string="Amount Revaluation",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="company_currency_id",
    )
    amount_diff = fields.Monetary(
        string="Unrealized Gain/Loss",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="company_currency_id",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )

    @api.model
    def _get_policy_field(self):
        res = super(AccountCurrencyRevaluation, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "company_id",
    )
    def onchange_gain_account_id(self):
        self.gain_account_id = False
        if self.company_id:
            self.gain_account_id = self.company_id.unrealized_gain_account_id

    @api.onchange(
        "company_id",
    )
    def onchange_loss_account_id(self):
        self.loss_account_id = False
        if self.company_id:
            self.loss_account_id = self.company_id.unrealized_loss_account_id

    @api.onchange(
        "company_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.company_id:
            self.journal_id = self.company_id.unrealized_journal_id

    def action_reload_accounting_entry(self):
        for record in self:
            record._reload_accounting_entry()

    def _reload_accounting_entry(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        self.line_ids.write({"currency_revaluation_id": False})
        criteria = [
            ("account_id", "=", self.account_id.id),
            ("currency_revaluation_id", "=", False),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
        ]
        lines = obj_line.search(criteria)
        if len(lines) > 0:
            lines.write(
                {
                    "currency_revaluation_id": self.id,
                }
            )

    @api.onchange(
        "account_id",
    )
    def onchange_currency_id(self):
        self.currency_id = False
        if self.account_id and self.account_id.currency_id:
            self.currency_id = self.account_id.currency_id

    def _prepare_account_move(self):
        self.ensure_one()
        lines = []
        lines.append((0, 0, self._prepare_debit_move_line()))
        lines.append((0, 0, self._prepare_credit_move_line()))
        return {
            "name": self.name,
            "journal_id": self.journal_id.id,
            "date": self.date,
            "line_ids": lines,
        }

    def _prepare_account_move_line(
        self,
        name,
        account,
        debit,
        credit,
        analytic_account=False,
        currency=False,
        amount_currency=0.0,
    ):
        self.ensure_one()
        return {
            "name": self.name,
            "account_id": account.id,
            "debit": debit,
            "credit": credit,
            "analytic_account_id": analytic_account and analytic_account.id or False,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
        }

    def _prepare_debit_move_line(self):
        self.ensure_one()
        return self._prepare_account_move_line(
            name="Revaluation",
            account=self._get_debit_account(),
            debit=abs(self.amount_diff),
            credit=0.0,
            analytic_account=self.analytic_account_id,
            currency=self.currency_id,
            amount_currency=0.0,
        )

    def _prepare_credit_move_line(self):
        self.ensure_one()
        return self._prepare_account_move_line(
            name="Revaluation",
            account=self._get_credit_account(),
            credit=abs(self.amount_diff),
            debit=0.0,
            analytic_account=self.analytic_account_id,
            currency=self.currency_id,
            amount_currency=0.0,
        )

    def _get_debit_account(self):
        self.ensure_one()
        if self.amount_diff > 0:
            return self.account_id
        else:
            return self.loss_account_id

    def _get_credit_account(self):
        self.ensure_one()
        if self.amount_diff > 0:
            return self.gain_account_id
        else:
            return self.account_id

    def _create_accounting_entry(self):
        self.ensure_one()
        Move = self.env["account.move"]
        # raise UserError(str(self._prepare_account_move()))
        return Move.create(self._prepare_account_move())

    def _prepare_done_data(self):
        _super = super(AccountCurrencyRevaluation, self)
        result = _super._prepare_done_data()
        result.update(
            {
                "move_id": self._create_accounting_entry().id,
            }
        )
        return result

    def action_cancel(self, cancel_reason_id=False):
        _super = super(AccountCurrencyRevaluation, self)
        _super.action_cancel(cancel_reason_id)
        for record in self:
            if record.move_id:
                move = record.move_id
                record.write(
                    {
                        "move_id": False,
                    }
                )
                move.with_context(force_delete=True).unlink()

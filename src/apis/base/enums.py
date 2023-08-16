from enum import StrEnum


class ModelPrefixEnum(StrEnum):
    AUTHORIZATION_GRANT = 'auth_grant_'
    BRANCH = 'branch_'
    CARD = 'card_'
    DEPARTMENT = 'dept_'
    FEATURE = 'feat_'
    GROUP = 'grp_'
    MODULE_PERMISSION = 'mod_perm_'
    PAYROLL = 'pyrl_'
    PAYSLIP = 'pyrl_slip_'
    PAYSLIP_HISTORY = 'pyslip_hist_'
    PAYROLL_BENEFIT = 'pyrl_benft_'
    PAYROLL_BONUS = 'pyrl_bns_'
    PAYROLL_DEDUCTION = 'pyrl_ddct_'
    PAYROLL_SETUP = 'pyrl_setup_'
    PAYROLL_SALARY_COMPONENT = 'pyrl_sal_comp_'
    TENANT = 'tenant_'
    USER = 'user_'
    WALLET = 'wal_'
    TRANSACTION = 'trxn_'

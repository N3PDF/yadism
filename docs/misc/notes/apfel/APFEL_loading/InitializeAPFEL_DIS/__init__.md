# InitializeAPFEL_DIS

- **Read input parameters:** initParametersDIS
  - if not already set initialize parameters to default
  - check the consistency of some inputs
  - see [initParametersDIS](./initParametersDIS.md)
- **Initialize the APFEL evolution:** InitializeAPFEL
  - *Read input parameters:* initParameters
  - *Report DIS parameters:* ReportParameters
  - *Initialize alphas grid:* initGridAlpha
  - for igrid in range(ngrid):
    - *Initialize x-space grid:* initGrid
    - *Flavour Number Scheme*:
    - *Evaluate evolution operators on the grid:*
  - end for
  - *if Welcome:* print time spent to initialize
  - see [InitializeAPFEL](./InitializeAPFEL/__init__.md)
- **Report DIS parameters:** ReportParametersDIS
  - *if Welcome:*
    - print EW parameters
    - print DIS parameters
- **Evaluate DIS or SIA integrals on the grid:**
  - if TimeLike
    - for igrid in (1,ngrid): initIntegralsSIA
  - else
    - for igrid in (1,ngrid): initIntegralsDIS
    - if Smallx: initIntegralsDISRes
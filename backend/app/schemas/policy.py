from pydantic import BaseModel


class DeploymentPolicyRequest(BaseModel):
    environment_id: str


class PolicyViolationRead(BaseModel):
    code: str
    severity: str
    message: str
    blocking: bool


class PolicyEvaluationRead(BaseModel):
    status: str
    violations: list[PolicyViolationRead]

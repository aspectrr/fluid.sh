# coding: utf-8

"""
Unified VirshSandbox Client

This module provides a unified client wrapper for the virsh-sandbox SDK,
offering a cleaner interface with flattened parameters instead of request objects.

Example:
    from virsh_sandbox import VirshSandbox

    client = VirshSandbox(host="http://localhost:8080")
    # Create a sandbox with simple parameters
    client.sandbox.create_sandbox(source_vm_name="ubuntu-base")
    # Run a command
    client.command.run_command(command="ls", args=["-la"])
"""

from typing import Any, Dict, List, Optional, Union
from typing_extensions import TypedDict, NotRequired

from virsh_sandbox.api.access_api import AccessApi
from virsh_sandbox.api.ansible_api import AnsibleApi
from virsh_sandbox.api.audit_api import AuditApi
from virsh_sandbox.api.command_api import CommandApi
from virsh_sandbox.api.file_api import FileApi
from virsh_sandbox.api.health_api import HealthApi
from virsh_sandbox.api.human_api import HumanApi
from virsh_sandbox.api.plan_api import PlanApi
from virsh_sandbox.api.sandbox_api import SandboxApi
from virsh_sandbox.api.tmux_api import TmuxApi
from virsh_sandbox.api.vms_api import VMsApi
from virsh_sandbox.api_client import ApiClient
from virsh_sandbox.configuration import Configuration
from virsh_sandbox.models.internal_ansible_job_request import \
    InternalAnsibleJobRequest
from virsh_sandbox.models.internal_api_create_sandbox_session_request import \
    InternalApiCreateSandboxSessionRequest
from virsh_sandbox.models.internal_rest_create_sandbox_request import \
    InternalRestCreateSandboxRequest
from virsh_sandbox.models.internal_rest_diff_request import \
    InternalRestDiffRequest
from virsh_sandbox.models.internal_rest_inject_ssh_key_request import \
    InternalRestInjectSSHKeyRequest
from virsh_sandbox.models.internal_rest_publish_request import \
    InternalRestPublishRequest
from virsh_sandbox.models.internal_rest_run_command_request import \
    InternalRestRunCommandRequest
from virsh_sandbox.models.internal_rest_snapshot_request import \
    InternalRestSnapshotRequest
from virsh_sandbox.models.internal_rest_start_sandbox_request import \
    InternalRestStartSandboxRequest
from virsh_sandbox.models.tmux_client_internal_types_approve_request import \
    TmuxClientInternalTypesApproveRequest
from virsh_sandbox.models.tmux_client_internal_types_ask_human_request import \
    TmuxClientInternalTypesAskHumanRequest
from virsh_sandbox.models.tmux_client_internal_types_audit_query import \
    TmuxClientInternalTypesAuditQuery
from virsh_sandbox.models.tmux_client_internal_types_copy_file_request import \
    TmuxClientInternalTypesCopyFileRequest
from virsh_sandbox.models.tmux_client_internal_types_create_pane_request import \
    TmuxClientInternalTypesCreatePaneRequest
from virsh_sandbox.models.tmux_client_internal_types_create_plan_request import \
    TmuxClientInternalTypesCreatePlanRequest
from virsh_sandbox.models.tmux_client_internal_types_delete_file_request import \
    TmuxClientInternalTypesDeleteFileRequest
from virsh_sandbox.models.tmux_client_internal_types_edit_file_request import \
    TmuxClientInternalTypesEditFileRequest
from virsh_sandbox.models.tmux_client_internal_types_list_dir_request import \
    TmuxClientInternalTypesListDirRequest
from virsh_sandbox.models.tmux_client_internal_types_read_file_request import \
    TmuxClientInternalTypesReadFileRequest
from virsh_sandbox.models.tmux_client_internal_types_read_pane_request import \
    TmuxClientInternalTypesReadPaneRequest
from virsh_sandbox.models.tmux_client_internal_types_run_command_request import \
    TmuxClientInternalTypesRunCommandRequest
from virsh_sandbox.models.tmux_client_internal_types_send_keys_request import \
    TmuxClientInternalTypesSendKeysRequest
from virsh_sandbox.models.tmux_client_internal_types_step_status import \
    TmuxClientInternalTypesStepStatus
from virsh_sandbox.models.tmux_client_internal_types_switch_pane_request import \
    TmuxClientInternalTypesSwitchPaneRequest
from virsh_sandbox.models.tmux_client_internal_types_update_plan_request import \
    TmuxClientInternalTypesUpdatePlanRequest
from virsh_sandbox.models.tmux_client_internal_types_write_file_request import \
    TmuxClientInternalTypesWriteFileRequest
from virsh_sandbox.models.virsh_sandbox_internal_rest_request_access_request import \
    VirshSandboxInternalRestRequestAccessRequest
from virsh_sandbox.models.virsh_sandbox_internal_rest_revoke_certificate_request import \
    VirshSandboxInternalRestRevokeCertificateRequest
from virsh_sandbox.models.virsh_sandbox_internal_rest_session_end_request import \
    VirshSandboxInternalRestSessionEndRequest
from virsh_sandbox.models.virsh_sandbox_internal_rest_session_start_request import \
    VirshSandboxInternalRestSessionStartRequest


# =============================================================================
# TypedDict Definitions for Response Types
# =============================================================================


class SandboxDict(TypedDict, total=False):
    """Sandbox information dictionary."""
    id: str
    agent_id: str
    base_image: str
    created_at: str
    deleted_at: Optional[str]
    ip_address: Optional[str]
    job_id: str
    network: str
    sandbox_name: str
    state: str
    ttl_seconds: Optional[int]
    updated_at: str


class CreateSandboxResponseDict(TypedDict, total=False):
    """Response from create_sandbox."""
    sandbox: SandboxDict


class StartSandboxResponseDict(TypedDict, total=False):
    """Response from start_sandbox."""
    sandbox: SandboxDict


class SnapshotDict(TypedDict, total=False):
    """Snapshot information dictionary."""
    id: str
    name: str
    sandbox_id: str
    created_at: str
    kind: str


class SnapshotResponseDict(TypedDict, total=False):
    """Response from create_snapshot."""
    snapshot: SnapshotDict


class ChangeDiffDict(TypedDict, total=False):
    """Change diff information."""
    path: str
    change_type: str
    old_content: Optional[str]
    new_content: Optional[str]


class DiffResponseDict(TypedDict, total=False):
    """Response from diff_snapshots."""
    changes: List[ChangeDiffDict]
    packages: List[Dict[str, Any]]
    services: List[Dict[str, Any]]


class RunCommandResponseDict(TypedDict, total=False):
    """Response from run_command and run_sandbox_command."""
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool


class FileInfoDict(TypedDict, total=False):
    """File information dictionary."""
    name: str
    path: str
    size: int
    mode: str
    mod_time: str
    is_dir: bool


class ListDirectoryResponseDict(TypedDict, total=False):
    """Response from list_directory."""
    files: List[FileInfoDict]
    path: str


class ReadFileResponseDict(TypedDict, total=False):
    """Response from read_file."""
    content: str
    path: str
    lines: int
    truncated: bool


class WriteFileResponseDict(TypedDict, total=False):
    """Response from write_file."""
    path: str
    bytes_written: int
    success: bool


class CopyFileResponseDict(TypedDict, total=False):
    """Response from copy_file."""
    source: str
    destination: str
    success: bool


class DeleteFileResponseDict(TypedDict, total=False):
    """Response from delete_file."""
    path: str
    success: bool


class EditFileResponseDict(TypedDict, total=False):
    """Response from edit_file."""
    path: str
    replacements: int
    success: bool


class HealthComponentDict(TypedDict, total=False):
    """Health component information."""
    name: str
    status: str
    message: Optional[str]


class HealthResponseDict(TypedDict, total=False):
    """Response from get_health."""
    status: str
    components: List[HealthComponentDict]


class AskHumanResponseDict(TypedDict, total=False):
    """Response from ask_human."""
    approved: bool
    response: Optional[str]
    comment: Optional[str]
    approved_by: Optional[str]


class PendingApprovalDict(TypedDict, total=False):
    """Pending approval information."""
    request_id: str
    prompt: str
    action_type: str
    urgency: str
    context: Optional[str]
    alternatives: List[str]
    created_at: str
    timeout_secs: int
    status: str


class ListApprovalsResponseDict(TypedDict, total=False):
    """Response from list_pending_approvals."""
    approvals: List[PendingApprovalDict]


class PlanStepDict(TypedDict, total=False):
    """Plan step information."""
    description: str
    status: str
    result: Optional[str]
    error: Optional[str]


class PlanDict(TypedDict, total=False):
    """Plan information."""
    id: str
    name: str
    description: Optional[str]
    steps: List[PlanStepDict]
    status: str
    current_step: int
    created_at: str
    updated_at: str


class CreatePlanResponseDict(TypedDict, total=False):
    """Response from create_plan."""
    plan: PlanDict


class GetPlanResponseDict(TypedDict, total=False):
    """Response from get_plan."""
    plan: PlanDict


class ListPlansResponseDict(TypedDict, total=False):
    """Response from list_plans."""
    plans: List[PlanDict]


class UpdatePlanResponseDict(TypedDict, total=False):
    """Response from update_plan."""
    plan: PlanDict


class AnsibleJobDict(TypedDict, total=False):
    """Ansible job information."""
    job_id: str
    status: str
    playbook: str
    vm_name: str
    output: Optional[str]
    error: Optional[str]
    created_at: str
    updated_at: str


class AnsibleJobResponseDict(TypedDict, total=False):
    """Response from create_ansible_job."""
    job: AnsibleJobDict


class AuditEntryDict(TypedDict, total=False):
    """Audit entry information."""
    id: str
    timestamp: str
    action: str
    actor: str
    resource: str
    details: Dict[str, Any]


class AuditQueryResponseDict(TypedDict, total=False):
    """Response from query_audit_log."""
    entries: List[AuditEntryDict]
    total: int


class CaPublicKeyResponseDict(TypedDict, total=False):
    """Response from v1_access_ca_pubkey_get."""
    public_key: str


class CertificateDict(TypedDict, total=False):
    """Certificate information."""
    cert_id: str
    user_id: str
    sandbox_id: str
    certificate: str
    status: str
    created_at: str
    expires_at: str
    revoked_at: Optional[str]
    revoke_reason: Optional[str]


class CertificateResponseDict(TypedDict, total=False):
    """Response from v1_access_certificate_cert_id_get."""
    certificate: CertificateDict


class ListCertificatesResponseDict(TypedDict, total=False):
    """Response from v1_access_certificates_get."""
    certificates: List[CertificateDict]
    total: int


class RequestAccessResponseDict(TypedDict, total=False):
    """Response from v1_access_request_post."""
    certificate: str
    cert_id: str
    expires_at: str


class SessionDict(TypedDict, total=False):
    """Session information."""
    session_id: str
    certificate_id: str
    user_id: str
    sandbox_id: str
    source_ip: str
    started_at: str
    ended_at: Optional[str]
    end_reason: Optional[str]


class SessionStartResponseDict(TypedDict, total=False):
    """Response from v1_access_session_start_post."""
    session_id: str


class ListSessionsResponseDict(TypedDict, total=False):
    """Response from v1_access_sessions_get."""
    sessions: List[SessionDict]
    total: int


class SandboxSessionInfoDict(TypedDict, total=False):
    """Sandbox session information."""
    session_name: str
    sandbox_id: str
    sandbox_ip: str
    certificate: str
    created_at: str
    expires_at: str


class CreateSandboxSessionResponseDict(TypedDict, total=False):
    """Response from create_sandbox_session."""
    session: SandboxSessionInfoDict


class ListSandboxSessionsResponseDict(TypedDict, total=False):
    """Response from list_sandbox_sessions."""
    sessions: List[SandboxSessionInfoDict]


class VMInfoDict(TypedDict, total=False):
    """VM information."""
    name: str
    state: str
    uuid: str
    memory: int
    vcpus: int


class ListVMsResponseDict(TypedDict, total=False):
    """Response from list_virtual_machines."""
    vms: List[VMInfoDict]


class TmuxSessionInfoDict(TypedDict, total=False):
    """Tmux session information."""
    name: str
    created: str
    attached: bool
    windows: int


class TmuxWindowInfoDict(TypedDict, total=False):
    """Tmux window information."""
    index: int
    name: str
    active: bool
    panes: int


class TmuxPaneInfoDict(TypedDict, total=False):
    """Tmux pane information."""
    id: str
    index: int
    active: bool
    width: int
    height: int
    current_command: Optional[str]


class CreatePaneResponseDict(TypedDict, total=False):
    """Response from create_tmux_pane."""
    pane_id: str
    window_name: str


class ListPanesResponseDict(TypedDict, total=False):
    """Response from list_tmux_panes."""
    panes: List[TmuxPaneInfoDict]


class ReadPaneResponseDict(TypedDict, total=False):
    """Response from read_tmux_pane."""
    content: str
    pane_id: str


class SendKeysResponseDict(TypedDict, total=False):
    """Response from send_keys_to_pane."""
    success: bool


class SwitchPaneResponseDict(TypedDict, total=False):
    """Response from switch_tmux_pane."""
    success: bool


class KillSessionResponseDict(TypedDict, total=False):
    """Response from release_tmux_session."""
    success: bool


# =============================================================================
# Helper Functions
# =============================================================================


def _to_dict(response: Any) -> Any:
    """Convert a response object to a dictionary.

    If the response has a to_dict method, use it.
    If it's a list, convert each item.
    If it's already a dict or None, return as-is.

    Args:
        response: The response object to convert.

    Returns:
        A dictionary representation of the response.
    """
    if response is None:
        return None
    if isinstance(response, dict):
        return response
    if isinstance(response, list):
        return [_to_dict(item) for item in response]
    if hasattr(response, "to_dict"):
        return response.to_dict()
    return response


# =============================================================================
# Operation Classes
# =============================================================================


class AccessOperations:
    """Wrapper for AccessApi with simplified method signatures."""

    def __init__(self, api: AccessApi) -> None:
        self._api: AccessApi = api

    def v1_access_ca_pubkey_get(self) -> CaPublicKeyResponseDict:
        """Get the SSH CA public key.

        Returns:
            CaPublicKeyResponseDict: Dictionary containing the public key.
        """
        return _to_dict(self._api.v1_access_ca_pubkey_get())

    def v1_access_certificate_cert_id_delete(
        self,
        cert_id: str,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Revoke a certificate.

        Args:
            cert_id: The certificate ID to revoke.
            reason: Optional reason for revocation.

        Returns:
            Dict containing the revocation status.
        """
        request = VirshSandboxInternalRestRevokeCertificateRequest(
            reason=reason,
        )
        return _to_dict(self._api.v1_access_certificate_cert_id_delete(
            cert_id=cert_id, request=request
        ))

    def v1_access_certificate_cert_id_get(
        self,
        cert_id: str,
    ) -> CertificateResponseDict:
        """Get certificate details.

        Args:
            cert_id: The certificate ID to retrieve.

        Returns:
            CertificateResponseDict: Dictionary containing certificate details.
        """
        return _to_dict(self._api.v1_access_certificate_cert_id_get(cert_id=cert_id))

    def v1_access_certificates_get(
        self,
        sandbox_id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        active_only: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ListCertificatesResponseDict:
        """List certificates.

        Args:
            sandbox_id: Filter by sandbox ID.
            user_id: Filter by user ID.
            status: Filter by certificate status.
            active_only: Only return active certificates.
            limit: Maximum number of results.
            offset: Pagination offset.

        Returns:
            ListCertificatesResponseDict: Dictionary containing list of certificates.
        """
        return _to_dict(self._api.v1_access_certificates_get(
            sandbox_id=sandbox_id,
            user_id=user_id,
            status=status,
            active_only=active_only,
            limit=limit,
            offset=offset,
        ))

    def v1_access_request_post(
        self,
        public_key: Optional[str] = None,
        sandbox_id: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
        user_id: Optional[str] = None,
    ) -> RequestAccessResponseDict:
        """Request SSH access to a sandbox.

        Args:
            public_key: The user's SSH public key.
            sandbox_id: The target sandbox ID.
            ttl_minutes: Requested access duration (1-10 minutes).
            user_id: The requesting user's ID.

        Returns:
            RequestAccessResponseDict: Dictionary containing the signed certificate.
        """
        request = VirshSandboxInternalRestRequestAccessRequest(
            public_key=public_key,
            sandbox_id=sandbox_id,
            ttl_minutes=ttl_minutes,
            user_id=user_id,
        )
        return _to_dict(self._api.v1_access_request_post(request=request))

    def v1_access_session_end_post(
        self,
        reason: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record session end.

        Args:
            reason: Reason for ending the session.
            session_id: The session ID to end.

        Returns:
            Dict containing the operation status.
        """
        request = VirshSandboxInternalRestSessionEndRequest(
            reason=reason,
            session_id=session_id,
        )
        return _to_dict(self._api.v1_access_session_end_post(request=request))

    def v1_access_session_start_post(
        self,
        certificate_id: Optional[str] = None,
        source_ip: Optional[str] = None,
    ) -> SessionStartResponseDict:
        """Record session start.

        Args:
            certificate_id: The certificate ID for the session.
            source_ip: The source IP address.

        Returns:
            SessionStartResponseDict: Dictionary containing the session ID.
        """
        request = VirshSandboxInternalRestSessionStartRequest(
            certificate_id=certificate_id,
            source_ip=source_ip,
        )
        return _to_dict(self._api.v1_access_session_start_post(request=request))

    def v1_access_sessions_get(
        self,
        sandbox_id: Optional[str] = None,
        certificate_id: Optional[str] = None,
        user_id: Optional[str] = None,
        active_only: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> ListSessionsResponseDict:
        """List sessions.

        Args:
            sandbox_id: Filter by sandbox ID.
            certificate_id: Filter by certificate ID.
            user_id: Filter by user ID.
            active_only: Only return active sessions.
            limit: Maximum number of results.
            offset: Pagination offset.

        Returns:
            ListSessionsResponseDict: Dictionary containing list of sessions.
        """
        return _to_dict(self._api.v1_access_sessions_get(
            sandbox_id=sandbox_id,
            certificate_id=certificate_id,
            user_id=user_id,
            active_only=active_only,
            limit=limit,
            offset=offset,
        ))


class AnsibleOperations:
    """Wrapper for AnsibleApi with simplified method signatures."""

    def __init__(self, api: AnsibleApi) -> None:
        self._api: AnsibleApi = api

    def create_ansible_job(
        self,
        check: Optional[bool] = None,
        playbook: Optional[str] = None,
        vm_name: Optional[str] = None,
    ) -> AnsibleJobResponseDict:
        """Create Ansible job.

        Args:
            check: Run in check mode (dry-run).
            playbook: The playbook content or path.
            vm_name: The target VM name.

        Returns:
            AnsibleJobResponseDict: Dictionary containing job information.
        """
        request = InternalAnsibleJobRequest(
            check=check,
            playbook=playbook,
            vm_name=vm_name,
        )
        return _to_dict(self._api.create_ansible_job(request=request))

    def get_ansible_job(
        self,
        job_id: str,
    ) -> AnsibleJobDict:
        """Get Ansible job.

        Args:
            job_id: The job ID to retrieve.

        Returns:
            AnsibleJobDict: Dictionary containing job details.
        """
        return _to_dict(self._api.get_ansible_job(job_id=job_id))

    def stream_ansible_job_output(
        self,
        job_id: str,
    ) -> None:
        """Stream Ansible job output.

        Args:
            job_id: The job ID to stream output from.
        """
        return self._api.stream_ansible_job_output(job_id=job_id)


class AuditOperations:
    """Wrapper for AuditApi with simplified method signatures."""

    def __init__(self, api: AuditApi) -> None:
        self._api: AuditApi = api

    def get_audit_stats(self) -> Dict[str, Any]:
        """Get audit stats.

        Returns:
            Dict containing audit statistics.
        """
        return _to_dict(self._api.get_audit_stats())

    def query_audit_log(self) -> AuditQueryResponseDict:
        """Query audit log.

        Returns:
            AuditQueryResponseDict: Dictionary containing audit entries.
        """
        request = TmuxClientInternalTypesAuditQuery()
        return _to_dict(self._api.query_audit_log(request=request))


class CommandOperations:
    """Wrapper for CommandApi with simplified method signatures."""

    def __init__(self, api: CommandApi) -> None:
        self._api: CommandApi = api

    def get_allowed_commands(self) -> Dict[str, Any]:
        """Get allowed commands.

        Returns:
            Dict containing list of allowed commands.
        """
        return _to_dict(self._api.get_allowed_commands())

    def run_command(
        self,
        args: Optional[List[str]] = None,
        command: Optional[str] = None,
        dry_run: Optional[bool] = None,
        env: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        work_dir: Optional[str] = None,
    ) -> RunCommandResponseDict:
        """Run command.

        Args:
            args: Arguments as separate items.
            command: Executable name only.
            dry_run: If true, don't actually execute.
            env: Additional env vars (KEY=VALUE format).
            timeout: Seconds, 0 = default (30s).
            work_dir: Working directory.

        Returns:
            RunCommandResponseDict: Dictionary containing command output.
        """
        request = TmuxClientInternalTypesRunCommandRequest(
            args=args,
            command=command,
            dry_run=dry_run,
            env=env,
            timeout=timeout,
            work_dir=work_dir,
        )
        return _to_dict(self._api.run_command(request=request))


class FileOperations:
    """Wrapper for FileApi with simplified method signatures."""

    def __init__(self, api: FileApi) -> None:
        self._api: FileApi = api

    def check_file_exists(self) -> Dict[str, Any]:
        """Check if file exists.

        Returns:
            Dict containing existence status.
        """
        return _to_dict(self._api.check_file_exists(request={}))

    def copy_file(
        self,
        destination: Optional[str] = None,
        overwrite: Optional[bool] = None,
        source: Optional[str] = None,
    ) -> CopyFileResponseDict:
        """Copy file.

        Args:
            destination: Destination path.
            overwrite: Whether to overwrite existing file.
            source: Source path.

        Returns:
            CopyFileResponseDict: Dictionary containing copy status.
        """
        request = TmuxClientInternalTypesCopyFileRequest(
            destination=destination,
            overwrite=overwrite,
            source=source,
        )
        return _to_dict(self._api.copy_file(request=request))

    def delete_file(
        self,
        path: Optional[str] = None,
        recursive: Optional[bool] = None,
    ) -> DeleteFileResponseDict:
        """Delete file.

        Args:
            path: Path to delete.
            recursive: For directories, delete recursively.

        Returns:
            DeleteFileResponseDict: Dictionary containing deletion status.
        """
        request = TmuxClientInternalTypesDeleteFileRequest(
            path=path,
            recursive=recursive,
        )
        return _to_dict(self._api.delete_file(request=request))

    def edit_file(
        self,
        all: Optional[bool] = None,
        new_text: Optional[str] = None,
        old_text: Optional[str] = None,
        path: Optional[str] = None,
    ) -> EditFileResponseDict:
        """Edit file.

        Args:
            all: Replace all occurrences (default: first only).
            new_text: Replacement text.
            old_text: Text to find and replace.
            path: File path.

        Returns:
            EditFileResponseDict: Dictionary containing edit status.
        """
        request = TmuxClientInternalTypesEditFileRequest(
            all=all,
            new_text=new_text,
            old_text=old_text,
            path=path,
        )
        return _to_dict(self._api.edit_file(request=request))

    def get_file_hash(self) -> Dict[str, str]:
        """Get file hash.

        Returns:
            Dict containing the file hash.
        """
        return _to_dict(self._api.get_file_hash(request={}))

    def list_directory(
        self,
        max_depth: Optional[int] = None,
        path: Optional[str] = None,
        recursive: Optional[bool] = None,
    ) -> ListDirectoryResponseDict:
        """List directory contents.

        Args:
            max_depth: Maximum depth for recursive listing.
            path: Directory path.
            recursive: Whether to list recursively.

        Returns:
            ListDirectoryResponseDict: Dictionary containing directory listing.
        """
        request = TmuxClientInternalTypesListDirRequest(
            max_depth=max_depth,
            path=path,
            recursive=recursive,
        )
        return _to_dict(self._api.list_directory(request=request))

    def read_file(
        self,
        from_line: Optional[int] = None,
        max_lines: Optional[int] = None,
        path: Optional[str] = None,
        to_line: Optional[int] = None,
    ) -> ReadFileResponseDict:
        """Read file.

        Args:
            from_line: 1-indexed start line, 0 = start.
            max_lines: Maximum lines to read, 0 = no limit.
            path: File path.
            to_line: 1-indexed end line, 0 = end.

        Returns:
            ReadFileResponseDict: Dictionary containing file content.
        """
        request = TmuxClientInternalTypesReadFileRequest(
            from_line=from_line,
            max_lines=max_lines,
            path=path,
            to_line=to_line,
        )
        return _to_dict(self._api.read_file(request=request))

    def write_file(
        self,
        content: Optional[str] = None,
        create_dir: Optional[bool] = None,
        mode: Optional[str] = None,
        overwrite: Optional[bool] = None,
        path: Optional[str] = None,
    ) -> WriteFileResponseDict:
        """Write file.

        Args:
            content: File content.
            create_dir: Create parent directories if needed.
            mode: File mode (e.g., "0644").
            overwrite: Must be true to overwrite existing.
            path: File path.

        Returns:
            WriteFileResponseDict: Dictionary containing write status.
        """
        request = TmuxClientInternalTypesWriteFileRequest(
            content=content,
            create_dir=create_dir,
            mode=mode,
            overwrite=overwrite,
            path=path,
        )
        return _to_dict(self._api.write_file(request=request))


class HealthOperations:
    """Wrapper for HealthApi with simplified method signatures."""

    def __init__(self, api: HealthApi) -> None:
        self._api: HealthApi = api

    def get_health(self) -> HealthResponseDict:
        """Get health status.

        Returns:
            HealthResponseDict: Dictionary containing health status.
        """
        return _to_dict(self._api.get_health())


class HumanOperations:
    """Wrapper for HumanApi with simplified method signatures."""

    def __init__(self, api: HumanApi) -> None:
        self._api: HumanApi = api

    def ask_human(
        self,
        action_type: Optional[str] = None,
        alternatives: Optional[List[str]] = None,
        context: Optional[str] = None,
        prompt: Optional[str] = None,
        timeout_secs: Optional[int] = None,
        urgency: Optional[str] = None,
    ) -> AskHumanResponseDict:
        """Request human approval (blocking).

        Args:
            action_type: Category of action.
            alternatives: Suggested alternative actions.
            context: Additional context.
            prompt: Human-readable description.
            timeout_secs: Auto-reject after timeout, 0 = no timeout.
            urgency: Urgency level.

        Returns:
            AskHumanResponseDict: Dictionary containing approval response.
        """
        request = TmuxClientInternalTypesAskHumanRequest(
            action_type=action_type,
            alternatives=alternatives,
            context=context,
            prompt=prompt,
            timeout_secs=timeout_secs,
            urgency=urgency,
        )
        return _to_dict(self._api.ask_human(request=request))

    def ask_human_async(
        self,
        action_type: Optional[str] = None,
        alternatives: Optional[List[str]] = None,
        context: Optional[str] = None,
        prompt: Optional[str] = None,
        timeout_secs: Optional[int] = None,
        urgency: Optional[str] = None,
    ) -> Dict[str, str]:
        """Request human approval asynchronously.

        Args:
            action_type: Category of action.
            alternatives: Suggested alternative actions.
            context: Additional context.
            prompt: Human-readable description.
            timeout_secs: Auto-reject after timeout, 0 = no timeout.
            urgency: Urgency level.

        Returns:
            Dict containing the request_id for polling.
        """
        request = TmuxClientInternalTypesAskHumanRequest(
            action_type=action_type,
            alternatives=alternatives,
            context=context,
            prompt=prompt,
            timeout_secs=timeout_secs,
            urgency=urgency,
        )
        return _to_dict(self._api.ask_human_async(request=request))

    def cancel_approval(
        self,
        request_id: str,
    ) -> Dict[str, Any]:
        """Cancel approval.

        Args:
            request_id: The approval request ID to cancel.

        Returns:
            Dict containing cancellation status.
        """
        return _to_dict(self._api.cancel_approval(request_id=request_id))

    def get_pending_approval(
        self,
        request_id: str,
    ) -> PendingApprovalDict:
        """Get pending approval.

        Args:
            request_id: The approval request ID.

        Returns:
            PendingApprovalDict: Dictionary containing approval details.
        """
        return _to_dict(self._api.get_pending_approval(request_id=request_id))

    def list_pending_approvals(self) -> ListApprovalsResponseDict:
        """List pending approvals.

        Returns:
            ListApprovalsResponseDict: Dictionary containing pending approvals.
        """
        return _to_dict(self._api.list_pending_approvals())

    def respond_to_approval(
        self,
        approved: Optional[bool] = None,
        approved_by: Optional[str] = None,
        comment: Optional[str] = None,
        request_id: Optional[str] = None,
    ) -> AskHumanResponseDict:
        """Respond to approval.

        Args:
            approved: Whether to approve the request.
            approved_by: Who approved/rejected the request.
            comment: Optional comment.
            request_id: The approval request ID.

        Returns:
            AskHumanResponseDict: Dictionary containing the response.
        """
        request = TmuxClientInternalTypesApproveRequest(
            approved=approved,
            approved_by=approved_by,
            comment=comment,
            request_id=request_id,
        )
        return _to_dict(self._api.respond_to_approval(request=request))


class PlanOperations:
    """Wrapper for PlanApi with simplified method signatures."""

    def __init__(self, api: PlanApi) -> None:
        self._api: PlanApi = api

    def abort_plan(
        self,
        plan_id: str,
        request: Optional[object] = None,
    ) -> Dict[str, Any]:
        """Abort plan.

        Args:
            plan_id: The plan ID to abort.
            request: Optional request body.

        Returns:
            Dict containing abort status.
        """
        return _to_dict(self._api.abort_plan(plan_id=plan_id, request=request))

    def advance_plan_step(
        self,
        plan_id: str,
        request: Optional[object] = None,
    ) -> Dict[str, Any]:
        """Advance plan step.

        Args:
            plan_id: The plan ID.
            request: Optional request body.

        Returns:
            Dict containing the new step information.
        """
        return _to_dict(self._api.advance_plan_step(plan_id=plan_id, request=request))

    def create_plan(
        self,
        description: Optional[str] = None,
        name: Optional[str] = None,
        steps: Optional[List[str]] = None,
    ) -> CreatePlanResponseDict:
        """Create plan.

        Args:
            description: Plan description.
            name: Plan name.
            steps: List of step descriptions.

        Returns:
            CreatePlanResponseDict: Dictionary containing the created plan.
        """
        request = TmuxClientInternalTypesCreatePlanRequest(
            description=description,
            name=name,
            steps=steps,
        )
        return _to_dict(self._api.create_plan(request=request))

    def delete_plan(
        self,
        plan_id: str,
    ) -> Dict[str, Any]:
        """Delete plan.

        Args:
            plan_id: The plan ID to delete.

        Returns:
            Dict containing deletion status.
        """
        return _to_dict(self._api.delete_plan(plan_id=plan_id))

    def get_plan(
        self,
        plan_id: str,
    ) -> GetPlanResponseDict:
        """Get plan.

        Args:
            plan_id: The plan ID to retrieve.

        Returns:
            GetPlanResponseDict: Dictionary containing plan details.
        """
        return _to_dict(self._api.get_plan(plan_id=plan_id))

    def list_plans(self) -> ListPlansResponseDict:
        """List plans.

        Returns:
            ListPlansResponseDict: Dictionary containing list of plans.
        """
        return _to_dict(self._api.list_plans())

    def update_plan(
        self,
        error: Optional[str] = None,
        plan_id: Optional[str] = None,
        result: Optional[str] = None,
        status: Optional[TmuxClientInternalTypesStepStatus] = None,
        step_index: Optional[int] = None,
    ) -> UpdatePlanResponseDict:
        """Update plan.

        Args:
            error: Error message if step failed.
            plan_id: The plan ID.
            result: Step result.
            status: New step status.
            step_index: Index of step to update.

        Returns:
            UpdatePlanResponseDict: Dictionary containing updated plan.
        """
        request = TmuxClientInternalTypesUpdatePlanRequest(
            error=error,
            plan_id=plan_id,
            result=result,
            status=status,
            step_index=step_index,
        )
        return _to_dict(self._api.update_plan(request=request))


class SandboxOperations:
    """Wrapper for SandboxApi with simplified method signatures."""

    def __init__(self, api: SandboxApi) -> None:
        self._api: SandboxApi = api

    def create_sandbox(
        self,
        agent_id: Optional[str] = None,
        cpu: Optional[int] = None,
        memory_mb: Optional[int] = None,
        source_vm_name: Optional[str] = None,
        vm_name: Optional[str] = None,
    ) -> CreateSandboxResponseDict:
        """Create a new sandbox.

        Args:
            agent_id: Required agent identity.
            cpu: Optional CPU count; default from service config if <=0.
            memory_mb: Optional memory in MB; default from service config if <=0.
            source_vm_name: Required; name of existing VM in libvirt to clone from.
            vm_name: Optional; generated if empty.

        Returns:
            CreateSandboxResponseDict: Dictionary containing the created sandbox.
        """
        request = InternalRestCreateSandboxRequest(
            agent_id=agent_id,
            cpu=cpu,
            memory_mb=memory_mb,
            source_vm_name=source_vm_name,
            vm_name=vm_name,
        )
        return _to_dict(self._api.create_sandbox(request=request))

    def create_sandbox_session(
        self,
        sandbox_id: Optional[str] = None,
        session_name: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
    ) -> CreateSandboxSessionResponseDict:
        """Create sandbox session.

        Args:
            sandbox_id: The ID of the sandbox to connect to.
            session_name: Optional tmux session name (auto-generated if empty).
            ttl_minutes: Certificate TTL in minutes (1-10, default 5).

        Returns:
            CreateSandboxSessionResponseDict: Dictionary containing session info.
        """
        request = InternalApiCreateSandboxSessionRequest(
            sandbox_id=sandbox_id,
            session_name=session_name,
            ttl_minutes=ttl_minutes,
        )
        return _to_dict(self._api.create_sandbox_session(request=request))

    def create_snapshot(
        self,
        id: str,
        external: Optional[bool] = None,
        name: Optional[str] = None,
    ) -> SnapshotResponseDict:
        """Create snapshot.

        Args:
            id: Sandbox ID.
            external: Optional; default false (internal snapshot).
            name: Required snapshot name.

        Returns:
            SnapshotResponseDict: Dictionary containing snapshot info.
        """
        request = InternalRestSnapshotRequest(
            external=external,
            name=name,
        )
        return _to_dict(self._api.create_snapshot(id=id, request=request))

    def destroy_sandbox(
        self,
        id: str,
    ) -> None:
        """Destroy sandbox.

        Args:
            id: Sandbox ID to destroy.
        """
        return self._api.destroy_sandbox(id=id)

    def diff_snapshots(
        self,
        id: str,
        from_snapshot: Optional[str] = None,
        to_snapshot: Optional[str] = None,
    ) -> DiffResponseDict:
        """Diff snapshots.

        Args:
            id: Sandbox ID.
            from_snapshot: Required; source snapshot name.
            to_snapshot: Required; target snapshot name.

        Returns:
            DiffResponseDict: Dictionary containing diff information.
        """
        request = InternalRestDiffRequest(
            from_snapshot=from_snapshot,
            to_snapshot=to_snapshot,
        )
        return _to_dict(self._api.diff_snapshots(id=id, request=request))

    def generate_configuration(
        self,
        id: str,
        tool: str,
    ) -> None:
        """Generate configuration.

        Args:
            id: Sandbox ID.
            tool: Tool to generate configuration for.
        """
        return self._api.generate_configuration(id=id, tool=tool)

    def get_sandbox_session(
        self,
        session_name: str,
    ) -> SandboxSessionInfoDict:
        """Get sandbox session.

        Args:
            session_name: The session name to retrieve.

        Returns:
            SandboxSessionInfoDict: Dictionary containing session info.
        """
        return _to_dict(self._api.get_sandbox_session(session_name=session_name))

    def inject_ssh_key(
        self,
        id: str,
        public_key: Optional[str] = None,
        username: Optional[str] = None,
    ) -> None:
        """Inject SSH key into sandbox.

        Args:
            id: Sandbox ID.
            public_key: Required; the SSH public key.
            username: Required; target username (e.g., "root").
        """
        request = InternalRestInjectSSHKeyRequest(
            public_key=public_key,
            username=username,
        )
        return self._api.inject_ssh_key(id=id, request=request)

    def kill_sandbox_session(
        self,
        session_name: str,
    ) -> Dict[str, Any]:
        """Kill sandbox session.

        Args:
            session_name: The session name to kill.

        Returns:
            Dict containing the operation status.
        """
        return _to_dict(self._api.kill_sandbox_session(session_name=session_name))

    def list_sandbox_sessions(self) -> ListSandboxSessionsResponseDict:
        """List sandbox sessions.

        Returns:
            ListSandboxSessionsResponseDict: Dictionary containing sessions list.
        """
        return _to_dict(self._api.list_sandbox_sessions())

    def publish_changes(
        self,
        id: str,
        job_id: Optional[str] = None,
        message: Optional[str] = None,
        reviewers: Optional[List[str]] = None,
    ) -> None:
        """Publish changes.

        Args:
            id: Sandbox ID.
            job_id: Required job ID.
            message: Optional commit/PR message.
            reviewers: Optional list of reviewers.
        """
        request = InternalRestPublishRequest(
            job_id=job_id,
            message=message,
            reviewers=reviewers,
        )
        return self._api.publish_changes(id=id, request=request)

    def run_sandbox_command(
        self,
        id: str,
        command: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        private_key_path: Optional[str] = None,
        timeout_sec: Optional[int] = None,
        username: Optional[str] = None,
    ) -> RunCommandResponseDict:
        """Run command in sandbox.

        Args:
            id: Sandbox ID.
            command: Required command to run.
            env: Optional environment variables.
            private_key_path: Required; path on API host.
            timeout_sec: Optional; default from service config.
            username: Required username.

        Returns:
            RunCommandResponseDict: Dictionary containing command output.
        """
        request = InternalRestRunCommandRequest(
            command=command,
            env=env,
            private_key_path=private_key_path,
            timeout_sec=timeout_sec,
            username=username,
        )
        return _to_dict(self._api.run_sandbox_command(id=id, request=request))

    def sandbox_api_health(self) -> Dict[str, Any]:
        """Check sandbox API health.

        Returns:
            Dict containing health status.
        """
        return _to_dict(self._api.sandbox_api_health())

    def start_sandbox(
        self,
        id: str,
        wait_for_ip: Optional[bool] = None,
    ) -> StartSandboxResponseDict:
        """Start sandbox.

        Args:
            id: Sandbox ID.
            wait_for_ip: Optional; default false.

        Returns:
            StartSandboxResponseDict: Dictionary containing started sandbox info.
        """
        request = InternalRestStartSandboxRequest(
            wait_for_ip=wait_for_ip,
        )
        return _to_dict(self._api.start_sandbox(id=id, request=request))


class TmuxOperations:
    """Wrapper for TmuxApi with simplified method signatures."""

    def __init__(self, api: TmuxApi) -> None:
        self._api: TmuxApi = api

    def create_tmux_pane(
        self,
        command: Optional[str] = None,
        horizontal: Optional[bool] = None,
        new_window: Optional[bool] = None,
        session_name: Optional[str] = None,
        window_name: Optional[str] = None,
    ) -> CreatePaneResponseDict:
        """Create tmux pane.

        Args:
            command: Command to run in the pane.
            horizontal: False = vertical split.
            new_window: True = create new window instead of split.
            session_name: Target session name.
            window_name: Target window name.

        Returns:
            CreatePaneResponseDict: Dictionary containing pane info.
        """
        request = TmuxClientInternalTypesCreatePaneRequest(
            command=command,
            horizontal=horizontal,
            new_window=new_window,
            session_name=session_name,
            window_name=window_name,
        )
        return _to_dict(self._api.create_tmux_pane(request=request))

    def create_tmux_session(self) -> Dict[str, str]:
        """Create tmux session.

        Returns:
            Dict containing the session name.
        """
        return _to_dict(self._api.create_tmux_session(request={}))

    def kill_tmux_pane(
        self,
        pane_id: str,
    ) -> Dict[str, Any]:
        """Kill tmux pane.

        Args:
            pane_id: The pane ID to kill.

        Returns:
            Dict containing the operation status.
        """
        return _to_dict(self._api.kill_tmux_pane(pane_id=pane_id))

    def kill_tmux_session(
        self,
        session_name: str,
    ) -> Dict[str, Any]:
        """Kill tmux session.

        Args:
            session_name: The session name to kill.

        Returns:
            Dict containing the operation status.
        """
        return _to_dict(self._api.kill_tmux_session(session_name=session_name))

    def list_tmux_panes(
        self,
        session: Optional[str] = None,
    ) -> ListPanesResponseDict:
        """List tmux panes.

        Args:
            session: Optional session name to filter.

        Returns:
            ListPanesResponseDict: Dictionary containing panes list.
        """
        return _to_dict(self._api.list_tmux_panes(session=session))

    def list_tmux_sessions(self) -> List[TmuxSessionInfoDict]:
        """List tmux sessions.

        Returns:
            List of TmuxSessionInfoDict dictionaries.
        """
        return _to_dict(self._api.list_tmux_sessions())

    def list_tmux_windows(
        self,
        session: Optional[str] = None,
    ) -> List[TmuxWindowInfoDict]:
        """List tmux windows.

        Args:
            session: Optional session name to filter.

        Returns:
            List of TmuxWindowInfoDict dictionaries.
        """
        return _to_dict(self._api.list_tmux_windows(session=session))

    def read_tmux_pane(
        self,
        last_n_lines: Optional[int] = None,
        pane_id: Optional[str] = None,
    ) -> ReadPaneResponseDict:
        """Read tmux pane.

        Args:
            last_n_lines: 0 means all visible content.
            pane_id: The pane ID to read.

        Returns:
            ReadPaneResponseDict: Dictionary containing pane content.
        """
        request = TmuxClientInternalTypesReadPaneRequest(
            last_n_lines=last_n_lines,
            pane_id=pane_id,
        )
        return _to_dict(self._api.read_tmux_pane(request=request))

    def release_tmux_session(
        self,
        session_id: str,
    ) -> KillSessionResponseDict:
        """Release tmux session.

        Args:
            session_id: The session ID to release.

        Returns:
            KillSessionResponseDict: Dictionary containing release status.
        """
        return _to_dict(self._api.release_tmux_session(session_id=session_id))

    def send_keys_to_pane(
        self,
        key: Optional[str] = None,
        pane_id: Optional[str] = None,
    ) -> SendKeysResponseDict:
        """Send keys to tmux pane.

        Args:
            key: Key to send (must be from approved list).
            pane_id: Target pane ID.

        Returns:
            SendKeysResponseDict: Dictionary containing send status.
        """
        request = TmuxClientInternalTypesSendKeysRequest(
            key=key,
            pane_id=pane_id,
        )
        return _to_dict(self._api.send_keys_to_pane(request=request))

    def switch_tmux_pane(
        self,
        pane_id: Optional[str] = None,
    ) -> SwitchPaneResponseDict:
        """Switch tmux pane.

        Args:
            pane_id: Target pane ID.

        Returns:
            SwitchPaneResponseDict: Dictionary containing switch status.
        """
        request = TmuxClientInternalTypesSwitchPaneRequest(
            pane_id=pane_id,
        )
        return _to_dict(self._api.switch_tmux_pane(request=request))


class VMsOperations:
    """Wrapper for VMsApi with simplified method signatures."""

    def __init__(self, api: VMsApi) -> None:
        self._api: VMsApi = api

    def list_virtual_machines(self) -> ListVMsResponseDict:
        """List all VMs.

        Returns:
            ListVMsResponseDict: Dictionary containing VMs list.
        """
        return _to_dict(self._api.list_virtual_machines())


# =============================================================================
# Main Client Class
# =============================================================================


class VirshSandbox:
    """Unified client for the virsh-sandbox API.

    This class provides a single entry point for all virsh-sandbox API operations,
    with support for separate hosts for the main API and tmux API.
    All methods use flattened parameters instead of request objects.

    Args:
        host: Base URL for the main virsh-sandbox API.
        tmux_host: Base URL for the tmux API (defaults to host).
        api_key: Optional API key for authentication.
        access_token: Optional access token for authentication.
        username: Optional username for basic auth.
        password: Optional password for basic auth.
        verify_ssl: Whether to verify SSL certificates.
        ssl_ca_cert: Path to CA certificate file.
        retries: Number of retries for failed requests.

    Example:
        >>> from virsh_sandbox import VirshSandbox
        >>> client = VirshSandbox()
        >>> client.sandbox.create_sandbox(source_vm_name="base-vm")
    """

    def __init__(
        self,
        host: str = "http://localhost:8080",
        tmux_host: Optional[str] = None,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
        retries: Optional[int] = None,
    ) -> None:
        """Initialize the VirshSandbox client."""
        self._main_config: Configuration = Configuration(
            host=host,
            api_key={"Authorization": api_key} if api_key else None,
            access_token=access_token,
            username=username,
            password=password,
            ssl_ca_cert=ssl_ca_cert,
            retries=retries,
        )
        self._main_config.verify_ssl = verify_ssl
        self._main_api_client: ApiClient = ApiClient(configuration=self._main_config)

        tmux_host = tmux_host or host
        if tmux_host != host:
            self._tmux_config: Configuration = Configuration(
                host=tmux_host,
                api_key={"Authorization": api_key} if api_key else None,
                access_token=access_token,
                username=username,
                password=password,
                ssl_ca_cert=ssl_ca_cert,
                retries=retries,
            )
            self._tmux_config.verify_ssl = verify_ssl
            self._tmux_api_client: ApiClient = ApiClient(configuration=self._tmux_config)
        else:
            self._tmux_config = self._main_config
            self._tmux_api_client = self._main_api_client

        self._access: Optional[AccessOperations] = None
        self._ansible: Optional[AnsibleOperations] = None
        self._audit: Optional[AuditOperations] = None
        self._command: Optional[CommandOperations] = None
        self._file: Optional[FileOperations] = None
        self._health: Optional[HealthOperations] = None
        self._human: Optional[HumanOperations] = None
        self._plan: Optional[PlanOperations] = None
        self._sandbox: Optional[SandboxOperations] = None
        self._tmux: Optional[TmuxOperations] = None
        self._vms: Optional[VMsOperations] = None

    @property
    def access(self) -> AccessOperations:
        """Access AccessApi operations."""
        if self._access is None:
            api = AccessApi(api_client=self._main_api_client)
            self._access = AccessOperations(api)
        return self._access

    @property
    def ansible(self) -> AnsibleOperations:
        """Access AnsibleApi operations."""
        if self._ansible is None:
            api = AnsibleApi(api_client=self._main_api_client)
            self._ansible = AnsibleOperations(api)
        return self._ansible

    @property
    def audit(self) -> AuditOperations:
        """Access AuditApi operations."""
        if self._audit is None:
            api = AuditApi(api_client=self._tmux_api_client)
            self._audit = AuditOperations(api)
        return self._audit

    @property
    def command(self) -> CommandOperations:
        """Access CommandApi operations."""
        if self._command is None:
            api = CommandApi(api_client=self._tmux_api_client)
            self._command = CommandOperations(api)
        return self._command

    @property
    def file(self) -> FileOperations:
        """Access FileApi operations."""
        if self._file is None:
            api = FileApi(api_client=self._tmux_api_client)
            self._file = FileOperations(api)
        return self._file

    @property
    def health(self) -> HealthOperations:
        """Access HealthApi operations."""
        if self._health is None:
            api = HealthApi(api_client=self._tmux_api_client)
            self._health = HealthOperations(api)
        return self._health

    @property
    def human(self) -> HumanOperations:
        """Access HumanApi operations."""
        if self._human is None:
            api = HumanApi(api_client=self._tmux_api_client)
            self._human = HumanOperations(api)
        return self._human

    @property
    def plan(self) -> PlanOperations:
        """Access PlanApi operations."""
        if self._plan is None:
            api = PlanApi(api_client=self._tmux_api_client)
            self._plan = PlanOperations(api)
        return self._plan

    @property
    def sandbox(self) -> SandboxOperations:
        """Access SandboxApi operations."""
        if self._sandbox is None:
            api = SandboxApi(api_client=self._main_api_client)
            self._sandbox = SandboxOperations(api)
        return self._sandbox

    @property
    def tmux(self) -> TmuxOperations:
        """Access TmuxApi operations."""
        if self._tmux is None:
            api = TmuxApi(api_client=self._tmux_api_client)
            self._tmux = TmuxOperations(api)
        return self._tmux

    @property
    def vms(self) -> VMsOperations:
        """Access VMsApi operations."""
        if self._vms is None:
            api = VMsApi(api_client=self._main_api_client)
            self._vms = VMsOperations(api)
        return self._vms

    @property
    def configuration(self) -> Configuration:
        """Get the main API configuration."""
        return self._main_config

    @property
    def tmux_configuration(self) -> Configuration:
        """Get the tmux API configuration."""
        return self._tmux_config

    def set_debug(self, debug: bool) -> None:
        """Enable or disable debug mode.

        Args:
            debug: Whether to enable debug mode.
        """
        self._main_config.debug = debug
        if self._tmux_config is not self._main_config:
            self._tmux_config.debug = debug

    def close(self) -> None:
        """Close the API client connections."""
        if hasattr(self._main_api_client.rest_client, "close"):
            self._main_api_client.rest_client.close()  # type: ignore
        if self._tmux_api_client is not self._main_api_client:
            if hasattr(self._tmux_api_client.rest_client, "close"):
                self._tmux_api_client.rest_client.close()  # type: ignore

    def __enter__(self) -> "VirshSandbox":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Context manager exit."""
        self.close()

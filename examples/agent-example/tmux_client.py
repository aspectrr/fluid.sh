"""
High-level Python client for the tmux-client API.

This module provides a convenient wrapper around the generated OpenAPI SDK
with sensible defaults for interacting with the tmux-client API.

Usage:
    from tmux_client import TmuxClient

    with TmuxClient() as client:
        # Check health
        health = client.check_health()

        # List sessions
        sessions = client.list_sessions()

        # Read pane content
        content = client.read_pane(pane_id="%0", last_n_lines=50)

        # Run a command
        result = client.run_command("ls", args=["-la"])
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

# Add the tmux_sdk folder to the path so we can import directly
TMUX_SDK_PATH = Path(__file__).parent / "tmux_sdk"
sys.path.insert(0, str(TMUX_SDK_PATH))

from tmux_sdk import openapi_client
from tmux_sdk.openapi_client.api import (
    audit_api,
    command_api,
    file_api,
    health_api,
    human_api,
    plan_api,
    tmux_api,
)
from tmux_sdk.openapi_client.models import (
    TmuxClientInternalTypesAskHumanRequest,
    TmuxClientInternalTypesApproveRequest,
    TmuxClientInternalTypesAuditQuery,
    TmuxClientInternalTypesCopyFileRequest,
    TmuxClientInternalTypesCreatePaneRequest,
    TmuxClientInternalTypesCreatePlanRequest,
    TmuxClientInternalTypesDeleteFileRequest,
    TmuxClientInternalTypesEditFileRequest,
    TmuxClientInternalTypesListDirRequest,
    TmuxClientInternalTypesReadFileRequest,
    TmuxClientInternalTypesReadPaneRequest,
    TmuxClientInternalTypesRunCommandRequest,
    TmuxClientInternalTypesSendKeysRequest,
    TmuxClientInternalTypesSwitchPaneRequest,
    TmuxClientInternalTypesUpdatePlanRequest,
    TmuxClientInternalTypesWriteFileRequest,
)

if TYPE_CHECKING:
    from tmux_sdk.openapi_client.models import (
        TmuxClientInternalTypesAskHumanResponse,
        TmuxClientInternalTypesAuditQueryResponse,
        TmuxClientInternalTypesCopyFileResponse,
        TmuxClientInternalTypesCreatePaneResponse,
        TmuxClientInternalTypesCreatePlanResponse,
        TmuxClientInternalTypesDeleteFileResponse,
        TmuxClientInternalTypesEditFileResponse,
        TmuxClientInternalTypesHealthResponse,
        TmuxClientInternalTypesListApprovalsResponse,
        TmuxClientInternalTypesListDirResponse,
        TmuxClientInternalTypesListPanesResponse,
        TmuxClientInternalTypesListPlansResponse,
        TmuxClientInternalTypesGetPlanResponse,
        TmuxClientInternalTypesPendingApproval,
        TmuxClientInternalTypesReadFileResponse,
        TmuxClientInternalTypesReadPaneResponse,
        TmuxClientInternalTypesRunCommandResponse,
        TmuxClientInternalTypesSendKeysResponse,
        TmuxClientInternalTypesSwitchPaneResponse,
        TmuxClientInternalTypesUpdatePlanResponse,
        TmuxClientInternalTypesWriteFileResponse,
    )

# Re-export ApiException for convenience
from tmux_sdk.openapi_client.rest import ApiException

__all__ = ["TmuxClient", "ApiException"]


def create_api_client(
    host: str = "http://localhost:8081",
    debug: bool = False,
    verify_ssl: bool = True,
) -> openapi_client.ApiClient:
    """
    Create a configured API client instance.

    Args:
        host: Base URL of the tmux-client API
        debug: Enable debug logging
        verify_ssl: Whether to verify SSL certificates

    Returns:
        Configured ApiClient instance
    """
    configuration = openapi_client.Configuration(host=host)
    configuration.debug = debug
    configuration.verify_ssl = verify_ssl

    client = openapi_client.ApiClient(configuration)
    client.default_headers["User-Agent"] = "tmux-client-python-sdk/1.0"

    return client


class TmuxClient:
    """
    High-level client for the tmux-client API with nice defaults.

    This client wraps the auto-generated OpenAPI SDK and provides
    a cleaner interface for common operations.

    Example:
        with TmuxClient() as client:
            # Check if API is healthy
            health = client.check_health()

            # List tmux sessions
            sessions = client.list_sessions()

            # Read pane content
            content = client.read_pane(pane_id="%0", last_n_lines=100)

            # Run a command
            result = client.run_command("git", args=["status"])

            # Edit a file
            client.edit_file(
                path="/path/to/file.txt",
                old_text="foo",
                new_text="bar",
            )
    """

    def __init__(
        self,
        host: str = "http://localhost:8081",
        debug: bool = False,
        verify_ssl: bool = True,
    ):
        """
        Initialize the client.

        Args:
            host: Base URL of the tmux-client API
            debug: Enable debug logging
            verify_ssl: Whether to verify SSL certificates
        """
        self._client = create_api_client(
            host=host,
            debug=debug,
            verify_ssl=verify_ssl,
        )

        # Initialize API instances
        self._audit_api = audit_api.AuditApi(self._client)
        self._command_api = command_api.CommandApi(self._client)
        self._file_api = file_api.FileApi(self._client)
        self._health_api = health_api.HealthApi(self._client)
        self._human_api = human_api.HumanApi(self._client)
        self._plan_api = plan_api.PlanApi(self._client)
        self._tmux_api = tmux_api.TmuxApi(self._client)

    def __enter__(self) -> "TmuxClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying API client and release resources."""
        if self._client:
            self._client.close()

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    def check_health(self) -> "TmuxClientInternalTypesHealthResponse":
        """
        Check API health status.

        Returns:
            Health status including component health
        """
        return self._health_api.v1_health_get()

    # -------------------------------------------------------------------------
    # Tmux Sessions
    # -------------------------------------------------------------------------

    def list_sessions(self) -> list:
        """
        List all tmux sessions.

        Returns:
            List of session info objects
        """
        return self._tmux_api.v1_tmux_sessions_get()

    def create_session(
        self,
        name: str | None = None,
        window_name: str | None = None,
        start_command: str | None = None,
    ) -> dict:
        """
        Create a new tmux session.

        Args:
            name: Optional session name
            window_name: Optional initial window name
            start_command: Optional command to run in the initial window

        Returns:
            Created session info
        """
        return self._tmux_api.v1_tmux_sessions_create_post(
            request={
                "name": name,
                "window_name": window_name,
                "start_command": start_command,
            }
        )

    def kill_session(self, session_name: str) -> "TmuxClientInternalTypesKillSessionResponse":
        """
        Kill a tmux session.

        Args:
            session_name: Name of the session to kill

        Returns:
            Response confirming the session was killed
        """
        return self._tmux_api.v1_tmux_sessions_session_name_delete(session_name)

    def release_session(self, session_id: str) -> None:
        """
        Release a tmux session.

        Args:
            session_id: ID of the session to release
        """
        return self._tmux_api.v1_tmux_sessions_session_id_release_post(session_id)

    # -------------------------------------------------------------------------
    # Tmux Windows
    # -------------------------------------------------------------------------

    def list_windows(self) -> list:
        """
        List all tmux windows.

        Returns:
            List of window info objects
        """
        return self._tmux_api.v1_tmux_windows_get()

    # -------------------------------------------------------------------------
    # Tmux Panes
    # -------------------------------------------------------------------------

    def list_panes(self) -> "TmuxClientInternalTypesListPanesResponse":
        """
        List all tmux panes.

        Returns:
            Response containing list of pane info objects
        """
        return self._tmux_api.v1_tmux_panes_get()

    def create_pane(
        self,
        target_pane: str | None = None,
        vertical: bool = False,
        start_command: str | None = None,
        size: int | None = None,
    ) -> "TmuxClientInternalTypesCreatePaneResponse":
        """
        Create a new tmux pane.

        Args:
            target_pane: Target pane to split
            vertical: Whether to split vertically (default: horizontal)
            start_command: Optional command to run in the new pane
            size: Optional size percentage for the new pane

        Returns:
            Created pane info
        """
        request = TmuxClientInternalTypesCreatePaneRequest(
            target_pane=target_pane,
            vertical=vertical,
            start_command=start_command,
            size=size,
        )
        return self._tmux_api.v1_tmux_panes_create_post(request)

    def read_pane(
        self,
        pane_id: str,
        last_n_lines: int | None = None,
        start_line: int | None = None,
        end_line: int | None = None,
    ) -> "TmuxClientInternalTypesReadPaneResponse":
        """
        Read content from a tmux pane.

        Args:
            pane_id: The pane ID (e.g., "%0")
            last_n_lines: Read the last N lines
            start_line: Start line number
            end_line: End line number

        Returns:
            Pane content
        """
        request = TmuxClientInternalTypesReadPaneRequest(
            pane_id=pane_id,
            last_n_lines=last_n_lines,
            start_line=start_line,
            end_line=end_line,
        )
        return self._tmux_api.v1_tmux_panes_read_post(request)

    def send_keys(
        self,
        pane_id: str,
        keys: str,
        literal: bool = False,
    ) -> "TmuxClientInternalTypesSendKeysResponse":
        """
        Send keys to a tmux pane.

        Args:
            pane_id: The pane ID
            keys: Keys to send (e.g., "Enter", "C-c")
            literal: Whether to send keys literally

        Returns:
            Response confirming keys were sent
        """
        request = TmuxClientInternalTypesSendKeysRequest(
            pane_id=pane_id,
            keys=keys,
            literal=literal,
        )
        return self._tmux_api.v1_tmux_panes_send_keys_post(request)

    def switch_pane(self, pane_id: str) -> "TmuxClientInternalTypesSwitchPaneResponse":
        """
        Switch to a tmux pane.

        Args:
            pane_id: The pane ID to switch to

        Returns:
            Response confirming pane switch
        """
        request = TmuxClientInternalTypesSwitchPaneRequest(pane_id=pane_id)
        return self._tmux_api.v1_tmux_panes_switch_post(request)

    def kill_pane(self, pane_id: str) -> None:
        """
        Kill a tmux pane.

        Args:
            pane_id: The pane ID to kill
        """
        return self._tmux_api.v1_tmux_panes_pane_id_delete(pane_id)

    # -------------------------------------------------------------------------
    # Command Execution
    # -------------------------------------------------------------------------

    def run_command(
        self,
        command: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        cwd: str | None = None,
        timeout: int | None = None,
        dry_run: bool = False,
    ) -> "TmuxClientInternalTypesRunCommandResponse":
        """
        Run a command.

        Args:
            command: Command to execute
            args: Command arguments
            env: Environment variables
            cwd: Working directory
            timeout: Timeout in seconds
            dry_run: If true, don't actually run the command

        Returns:
            Command execution result with stdout, stderr, exit_code
        """
        request = TmuxClientInternalTypesRunCommandRequest(
            command=command,
            args=args,
            env=env,
            cwd=cwd,
            timeout=timeout,
            dry_run=dry_run,
        )
        return self._command_api.v1_command_run_post(request)

    def get_allowed_commands(self) -> dict:
        """
        Get the list of allowed and denied commands.

        Returns:
            Dictionary with allowed and denied command patterns
        """
        return self._command_api.v1_command_allowed_get()

    # -------------------------------------------------------------------------
    # File Operations
    # -------------------------------------------------------------------------

    def read_file(
        self,
        path: str,
        start_line: int | None = None,
        end_line: int | None = None,
    ) -> "TmuxClientInternalTypesReadFileResponse":
        """
        Read a file.

        Args:
            path: File path
            start_line: Optional start line
            end_line: Optional end line

        Returns:
            File content
        """
        request = TmuxClientInternalTypesReadFileRequest(
            path=path,
            start_line=start_line,
            end_line=end_line,
        )
        return self._file_api.v1_file_read_post(request)

    def write_file(
        self,
        path: str,
        content: str,
        create_dirs: bool = False,
        mode: str | None = None,
    ) -> "TmuxClientInternalTypesWriteFileResponse":
        """
        Write a file.

        Args:
            path: File path
            content: File content
            create_dirs: Whether to create parent directories
            mode: Optional file mode (e.g., "0644")

        Returns:
            Write result
        """
        request = TmuxClientInternalTypesWriteFileRequest(
            path=path,
            content=content,
            create_dirs=create_dirs,
            mode=mode,
        )
        return self._file_api.v1_file_write_post(request)

    def edit_file(
        self,
        path: str,
        old_text: str,
        new_text: str,
    ) -> "TmuxClientInternalTypesEditFileResponse":
        """
        Edit a file using find/replace.

        Args:
            path: File path
            old_text: Text to find
            new_text: Text to replace with

        Returns:
            Edit result with diff
        """
        request = TmuxClientInternalTypesEditFileRequest(
            path=path,
            old_text=old_text,
            new_text=new_text,
        )
        return self._file_api.v1_file_edit_post(request)

    def copy_file(
        self,
        source: str,
        destination: str,
    ) -> "TmuxClientInternalTypesCopyFileResponse":
        """
        Copy a file.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            Copy result
        """
        request = TmuxClientInternalTypesCopyFileRequest(
            source=source,
            destination=destination,
        )
        return self._file_api.v1_file_copy_post(request)

    def delete_file(self, path: str) -> "TmuxClientInternalTypesDeleteFileResponse":
        """
        Delete a file.

        Args:
            path: File path to delete

        Returns:
            Delete result
        """
        request = TmuxClientInternalTypesDeleteFileRequest(path=path)
        return self._file_api.v1_file_delete_post(request)

    def list_directory(
        self,
        path: str,
        recursive: bool = False,
    ) -> "TmuxClientInternalTypesListDirResponse":
        """
        List directory contents.

        Args:
            path: Directory path
            recursive: Whether to list recursively

        Returns:
            Directory listing with file info
        """
        request = TmuxClientInternalTypesListDirRequest(
            path=path,
            recursive=recursive,
        )
        return self._file_api.v1_file_list_post(request)

    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists.

        Args:
            path: File path

        Returns:
            True if the file exists
        """
        response = self._file_api.v1_file_exists_post(path=path)
        return response.exists if hasattr(response, 'exists') else bool(response)

    def get_file_hash(self, path: str) -> str:
        """
        Get the hash of a file.

        Args:
            path: File path

        Returns:
            File hash
        """
        response = self._file_api.v1_file_hash_post(path=path)
        return response.hash if hasattr(response, 'hash') else str(response)

    # -------------------------------------------------------------------------
    # Human Approval
    # -------------------------------------------------------------------------

    def ask_human(
        self,
        prompt: str,
        action_type: str | None = None,
        urgency: str | None = None,
        timeout_secs: int | None = None,
    ) -> "TmuxClientInternalTypesAskHumanResponse":
        """
        Request human approval (blocking).

        Args:
            prompt: The prompt/question to display
            action_type: Type of action (e.g., "destructive")
            urgency: Urgency level
            timeout_secs: Timeout in seconds

        Returns:
            Approval response
        """
        request = TmuxClientInternalTypesAskHumanRequest(
            prompt=prompt,
            action_type=action_type,
            urgency=urgency,
            timeout_secs=timeout_secs,
        )
        return self._human_api.v1_human_ask_post(request)

    def ask_human_async(
        self,
        prompt: str,
        action_type: str | None = None,
        urgency: str | None = None,
        timeout_secs: int | None = None,
    ) -> "TmuxClientInternalTypesAskHumanResponse":
        """
        Request human approval (async/non-blocking).

        Args:
            prompt: The prompt/question to display
            action_type: Type of action
            urgency: Urgency level
            timeout_secs: Timeout in seconds

        Returns:
            Response with request_id for polling
        """
        request = TmuxClientInternalTypesAskHumanRequest(
            prompt=prompt,
            action_type=action_type,
            urgency=urgency,
            timeout_secs=timeout_secs,
        )
        return self._human_api.v1_human_ask_async_post(request)

    def list_pending_approvals(self) -> "TmuxClientInternalTypesListApprovalsResponse":
        """
        List pending approval requests.

        Returns:
            List of pending approvals
        """
        return self._human_api.v1_human_pending_get()

    def get_pending_approval(self, request_id: str) -> "TmuxClientInternalTypesPendingApproval":
        """
        Get a specific pending approval.

        Args:
            request_id: The approval request ID

        Returns:
            Pending approval details
        """
        return self._human_api.v1_human_pending_request_id_get(request_id)

    def respond_to_approval(
        self,
        request_id: str,
        approved: bool,
        approved_by: str | None = None,
        comment: str | None = None,
    ) -> None:
        """
        Respond to an approval request.

        Args:
            request_id: The approval request ID
            approved: Whether to approve
            approved_by: Who approved (e.g., email)
            comment: Optional comment
        """
        request = TmuxClientInternalTypesApproveRequest(
            request_id=request_id,
            approved=approved,
            approved_by=approved_by,
            comment=comment,
        )
        return self._human_api.v1_human_respond_post(request)

    def cancel_approval(self, request_id: str) -> None:
        """
        Cancel a pending approval request.

        Args:
            request_id: The approval request ID
        """
        return self._human_api.v1_human_pending_request_id_delete(request_id)

    # -------------------------------------------------------------------------
    # Plans
    # -------------------------------------------------------------------------

    def create_plan(
        self,
        name: str,
        steps: list[str],
        description: str | None = None,
    ) -> "TmuxClientInternalTypesCreatePlanResponse":
        """
        Create a new execution plan.

        Args:
            name: Plan name
            steps: List of step descriptions
            description: Optional plan description

        Returns:
            Created plan info
        """
        request = TmuxClientInternalTypesCreatePlanRequest(
            name=name,
            steps=steps,
            description=description,
        )
        return self._plan_api.v1_plan_create_post(request)

    def list_plans(self) -> "TmuxClientInternalTypesListPlansResponse":
        """
        List all plans.

        Returns:
            List of plans
        """
        return self._plan_api.v1_plan_get()

    def get_plan(self, plan_id: str) -> "TmuxClientInternalTypesGetPlanResponse":
        """
        Get a specific plan.

        Args:
            plan_id: The plan ID

        Returns:
            Plan details
        """
        return self._plan_api.v1_plan_plan_id_get(plan_id)

    def update_plan(
        self,
        plan_id: str,
        step_index: int,
        status: str,
        output: str | None = None,
    ) -> "TmuxClientInternalTypesUpdatePlanResponse":
        """
        Update a plan step.

        Args:
            plan_id: The plan ID
            step_index: Step index to update
            status: New status
            output: Optional output/result

        Returns:
            Updated plan
        """
        request = TmuxClientInternalTypesUpdatePlanRequest(
            plan_id=plan_id,
            step_index=step_index,
            status=status,
            output=output,
        )
        return self._plan_api.v1_plan_update_post(request)

    def advance_plan(self, plan_id: str) -> "TmuxClientInternalTypesUpdatePlanResponse":
        """
        Advance to the next step in a plan.

        Args:
            plan_id: The plan ID

        Returns:
            Updated plan
        """
        return self._plan_api.v1_plan_plan_id_advance_post(plan_id)

    def abort_plan(self, plan_id: str) -> None:
        """
        Abort a plan.

        Args:
            plan_id: The plan ID
        """
        return self._plan_api.v1_plan_plan_id_abort_post(plan_id)

    def delete_plan(self, plan_id: str) -> None:
        """
        Delete a plan.

        Args:
            plan_id: The plan ID
        """
        return self._plan_api.v1_plan_plan_id_delete(plan_id)

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    def query_audit_log(
        self,
        tool: str | None = None,
        action: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int | None = None,
    ) -> "TmuxClientInternalTypesAuditQueryResponse":
        """
        Query the audit log.

        Args:
            tool: Filter by tool name
            action: Filter by action
            since: Filter by start time (ISO 8601)
            until: Filter by end time (ISO 8601)
            limit: Maximum number of results

        Returns:
            Matching audit entries
        """
        request = TmuxClientInternalTypesAuditQuery(
            tool=tool,
            action=action,
            since=since,
            until=until,
            limit=limit,
        )
        return self._audit_api.v1_audit_query_post(request=request)

    def get_audit_stats(self) -> dict:
        """
        Get audit statistics.

        Returns:
            Audit statistics
        """
        return self._audit_api.v1_audit_stats_get()

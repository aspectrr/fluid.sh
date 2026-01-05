# coding: utf-8

"""
Tests for the VirshSandbox unified client.

This module tests that all client methods properly return Pydantic model
objects with full IDE autocomplete support.
"""

import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from pydantic import BaseModel

from virsh_sandbox.client import (AccessOperations, AnsibleOperations,
                                  AuditOperations, CommandOperations,
                                  FileOperations, HealthOperations,
                                  HumanOperations, PlanOperations,
                                  SandboxOperations, TmuxOperations,
                                  VirshSandbox, VMsOperations)


class MockPydanticModel(BaseModel):
    """Mock Pydantic model for testing."""

    id: str = ""
    name: str = ""


class TestAccessOperations(unittest.TestCase):
    """Test AccessOperations wrapper methods return Pydantic models."""

    def test_v1_access_ca_pubkey_get_returns_model(self) -> None:
        """Test v1_access_ca_pubkey_get returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_ca_pubkey_get.return_value = MockPydanticModel(id="test")
        ops = AccessOperations(mock_api)
        result = ops.v1_access_ca_pubkey_get()
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_certificate_cert_id_delete_returns_model(self) -> None:
        """Test delete certificate returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_certificate_cert_id_delete.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_certificate_cert_id_delete(cert_id="test-cert")
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_certificate_cert_id_get_returns_model(self) -> None:
        """Test get certificate returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_certificate_cert_id_get.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_certificate_cert_id_get(cert_id="test-cert")
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_certificates_get_returns_model(self) -> None:
        """Test list certificates returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_certificates_get.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_certificates_get()
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_request_post_returns_model(self) -> None:
        """Test request access returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_request_post.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_request_post()
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_session_end_post_returns_model(self) -> None:
        """Test session end returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_session_end_post.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_session_end_post()
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_session_start_post_returns_model(self) -> None:
        """Test session start returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_session_start_post.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_session_start_post()
        self.assertIsInstance(result, BaseModel)

    def test_v1_access_sessions_get_returns_model(self) -> None:
        """Test list sessions returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.v1_access_sessions_get.return_value = MockPydanticModel()
        ops = AccessOperations(mock_api)
        result = ops.v1_access_sessions_get()
        self.assertIsInstance(result, BaseModel)


class TestSandboxOperations(unittest.TestCase):
    """Test SandboxOperations wrapper methods return Pydantic models."""

    def test_create_sandbox_returns_model(self) -> None:
        """Test create_sandbox returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.create_sandbox.return_value = MockPydanticModel(id="SBX-123")
        ops = SandboxOperations(mock_api)
        result = ops.create_sandbox()
        self.assertIsInstance(result, BaseModel)

    def test_create_sandbox_session_returns_model(self) -> None:
        """Test create_sandbox_session returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.create_sandbox_session.return_value = MockPydanticModel()
        ops = SandboxOperations(mock_api)
        result = ops.create_sandbox_session()
        self.assertIsInstance(result, BaseModel)

    def test_start_sandbox_returns_model(self) -> None:
        """Test start_sandbox returns a Pydantic model."""
        mock_api = MagicMock()
        mock_api.start_sandbox.return_value = MockPydanticModel()
        ops = SandboxOperations(mock_api)
        result = ops.start_sandbox(id="SBX-123")
        self.assertIsInstance(result, BaseModel)


class TestVirshSandboxClient(unittest.TestCase):
    """Test the main VirshSandbox client."""

    @patch("virsh_sandbox.client.ApiClient")
    @patch("virsh_sandbox.client.Configuration")
    def test_client_initialization(
        self, mock_config: MagicMock, mock_api_client: MagicMock
    ) -> None:
        """Test client initializes with default parameters."""
        client = VirshSandbox(host="http://localhost:8080")
        self.assertIsNotNone(client)

    @patch("virsh_sandbox.client.ApiClient")
    @patch("virsh_sandbox.client.Configuration")
    def test_client_properties_return_operations(
        self, mock_config: MagicMock, mock_api_client: MagicMock
    ) -> None:
        """Test client properties return Operation instances."""
        client = VirshSandbox(host="http://localhost:8080")
        self.assertIsInstance(client.access, AccessOperations)
        self.assertIsInstance(client.ansible, AnsibleOperations)
        self.assertIsInstance(client.audit, AuditOperations)
        self.assertIsInstance(client.command, CommandOperations)
        self.assertIsInstance(client.file, FileOperations)
        self.assertIsInstance(client.health, HealthOperations)
        self.assertIsInstance(client.human, HumanOperations)
        self.assertIsInstance(client.plan, PlanOperations)
        self.assertIsInstance(client.sandbox, SandboxOperations)
        self.assertIsInstance(client.tmux, TmuxOperations)
        self.assertIsInstance(client.vms, VMsOperations)

    @patch("virsh_sandbox.client.ApiClient")
    @patch("virsh_sandbox.client.Configuration")
    def test_client_context_manager(
        self, mock_config: MagicMock, mock_api_client: MagicMock
    ) -> None:
        """Test client works as context manager."""
        with VirshSandbox(host="http://localhost:8080") as client:
            self.assertIsNotNone(client)

    @patch("virsh_sandbox.client.ApiClient")
    @patch("virsh_sandbox.client.Configuration")
    def test_client_with_separate_tmux_host(
        self, mock_config: MagicMock, mock_api_client: MagicMock
    ) -> None:
        """Test client with separate tmux host."""
        client = VirshSandbox(
            host="http://localhost:8080", tmux_host="http://localhost:8081"
        )
        self.assertIsNotNone(client)


class TestPydanticModelReturns(unittest.TestCase):
    """Test that Pydantic models provide IDE autocomplete benefits."""

    def test_model_has_fields(self) -> None:
        """Test that returned models have accessible fields."""
        model = MockPydanticModel(id="test-id", name="test-name")
        self.assertEqual(model.id, "test-id")
        self.assertEqual(model.name, "test-name")

    def test_model_dump_converts_to_dict(self) -> None:
        """Test that model_dump() converts to dict when needed."""
        model = MockPydanticModel(id="test-id", name="test-name")
        result = model.model_dump()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "test-id")
        self.assertEqual(result["name"], "test-name")

    def test_model_has_field_info(self) -> None:
        """Test that Pydantic models expose field information for IDE autocomplete."""
        # model_fields contains field definitions for IDE introspection
        self.assertIn("id", MockPydanticModel.model_fields)
        self.assertIn("name", MockPydanticModel.model_fields)


if __name__ == "__main__":
    unittest.main()

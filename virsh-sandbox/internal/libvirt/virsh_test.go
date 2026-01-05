//go:build libvirt
// +build libvirt

package libvirt

import (
	"strings"
	"testing"
)

func TestRenderDomainXML_CPUMode(t *testing.T) {
	tests := []struct {
		name            string
		params          domainXMLParams
		expectedCPUMode string
	}{
		{
			name: "x86_64 with kvm uses host-passthrough",
			params: domainXMLParams{
				Name:       "test-vm",
				MemoryMB:   1024,
				VCPUs:      2,
				DiskPath:   "/var/lib/libvirt/images/test.qcow2",
				Network:    "default",
				Arch:       "x86_64",
				Machine:    "pc-q35-6.2",
				DomainType: "kvm",
			},
			expectedCPUMode: `<cpu mode="host-passthrough"/>`,
		},
		{
			name: "x86_64 with qemu uses host-passthrough",
			params: domainXMLParams{
				Name:       "test-vm",
				MemoryMB:   1024,
				VCPUs:      2,
				DiskPath:   "/var/lib/libvirt/images/test.qcow2",
				Network:    "default",
				Arch:       "x86_64",
				Machine:    "pc-q35-6.2",
				DomainType: "qemu",
			},
			expectedCPUMode: `<cpu mode="host-passthrough"/>`,
		},
		{
			name: "aarch64 with kvm uses host-passthrough",
			params: domainXMLParams{
				Name:       "test-vm",
				MemoryMB:   1024,
				VCPUs:      2,
				DiskPath:   "/var/lib/libvirt/images/test.qcow2",
				Network:    "default",
				Arch:       "aarch64",
				Machine:    "virt",
				DomainType: "kvm",
			},
			expectedCPUMode: `<cpu mode="host-passthrough"/>`,
		},
		{
			name: "aarch64 with qemu uses custom cortex-a72 model",
			params: domainXMLParams{
				Name:       "test-vm",
				MemoryMB:   1024,
				VCPUs:      2,
				DiskPath:   "/var/lib/libvirt/images/test.qcow2",
				Network:    "default",
				Arch:       "aarch64",
				Machine:    "virt",
				DomainType: "qemu",
			},
			expectedCPUMode: `<cpu mode="custom" match="exact">`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			xml, err := renderDomainXML(tt.params)
			if err != nil {
				t.Fatalf("renderDomainXML() error = %v", err)
			}

			if !strings.Contains(xml, tt.expectedCPUMode) {
				t.Errorf("renderDomainXML() expected CPU mode %q not found in XML:\n%s", tt.expectedCPUMode, xml)
			}
		})
	}
}

func TestRenderDomainXML_BasicStructure(t *testing.T) {
	params := domainXMLParams{
		Name:       "test-sandbox",
		MemoryMB:   2048,
		VCPUs:      4,
		DiskPath:   "/var/lib/libvirt/images/test-sandbox.qcow2",
		Network:    "default",
		Arch:       "x86_64",
		Machine:    "pc-q35-6.2",
		DomainType: "kvm",
	}

	xml, err := renderDomainXML(params)
	if err != nil {
		t.Fatalf("renderDomainXML() error = %v", err)
	}

	expectedElements := []string{
		`<domain type="kvm">`,
		`<name>test-sandbox</name>`,
		`<memory unit="MiB">2048</memory>`,
		`<vcpu placement="static">4</vcpu>`,
		`<type arch="x86_64" machine="pc-q35-6.2">hvm</type>`,
		`<source file="/var/lib/libvirt/images/test-sandbox.qcow2"/>`,
		`<source network="default"/>`,
	}

	for _, expected := range expectedElements {
		if !strings.Contains(xml, expected) {
			t.Errorf("renderDomainXML() expected element %q not found in XML:\n%s", expected, xml)
		}
	}
}

func TestRenderDomainXML_Aarch64Features(t *testing.T) {
	params := domainXMLParams{
		Name:       "test-arm-vm",
		MemoryMB:   1024,
		VCPUs:      2,
		DiskPath:   "/var/lib/libvirt/images/test.qcow2",
		Network:    "default",
		Arch:       "aarch64",
		Machine:    "virt",
		DomainType: "qemu",
	}

	xml, err := renderDomainXML(params)
	if err != nil {
		t.Fatalf("renderDomainXML() error = %v", err)
	}

	// aarch64-specific elements
	expectedElements := []string{
		`<os firmware="efi">`,
		`<gic version="2"/>`,
		`<controller type="usb" model="qemu-xhci"/>`,
		`<cpu mode="custom" match="exact">`,
		`<model fallback="allow">cortex-a72</model>`,
	}

	for _, expected := range expectedElements {
		if !strings.Contains(xml, expected) {
			t.Errorf("renderDomainXML() expected aarch64 element %q not found in XML:\n%s", expected, xml)
		}
	}

	// x86_64-specific elements should NOT be present
	unexpectedElements := []string{
		`<apic/>`,
		`<pae/>`,
		`<input type="tablet" bus="usb"/>`,
	}

	for _, unexpected := range unexpectedElements {
		if strings.Contains(xml, unexpected) {
			t.Errorf("renderDomainXML() unexpected x86_64 element %q found in aarch64 XML:\n%s", unexpected, xml)
		}
	}
}

func TestRenderDomainXML_X86Features(t *testing.T) {
	params := domainXMLParams{
		Name:       "test-x86-vm",
		MemoryMB:   1024,
		VCPUs:      2,
		DiskPath:   "/var/lib/libvirt/images/test.qcow2",
		Network:    "default",
		Arch:       "x86_64",
		Machine:    "pc-q35-6.2",
		DomainType: "kvm",
	}

	xml, err := renderDomainXML(params)
	if err != nil {
		t.Fatalf("renderDomainXML() error = %v", err)
	}

	// x86_64-specific elements
	expectedElements := []string{
		`<apic/>`,
		`<pae/>`,
		`<input type="tablet" bus="usb"/>`,
	}

	for _, expected := range expectedElements {
		if !strings.Contains(xml, expected) {
			t.Errorf("renderDomainXML() expected x86_64 element %q not found in XML:\n%s", expected, xml)
		}
	}

	// aarch64-specific elements should NOT be present
	unexpectedElements := []string{
		`<os firmware="efi">`,
		`<gic version="2"/>`,
		`<controller type="usb" model="qemu-xhci"/>`,
	}

	for _, unexpected := range unexpectedElements {
		if strings.Contains(xml, unexpected) {
			t.Errorf("renderDomainXML() unexpected aarch64 element %q found in x86_64 XML:\n%s", unexpected, xml)
		}
	}
}

func TestRenderDomainXML_Defaults(t *testing.T) {
	// Test that defaults are applied when fields are empty
	params := domainXMLParams{
		Name:     "test-defaults",
		MemoryMB: 512,
		VCPUs:    1,
		DiskPath: "/var/lib/libvirt/images/test.qcow2",
		Network:  "default",
		// Arch, Machine, and DomainType are empty - should use defaults
	}

	xml, err := renderDomainXML(params)
	if err != nil {
		t.Fatalf("renderDomainXML() error = %v", err)
	}

	// Should default to x86_64, pc-q35-6.2, kvm
	expectedDefaults := []string{
		`<domain type="kvm">`,
		`<type arch="x86_64" machine="pc-q35-6.2">hvm</type>`,
		`<cpu mode="host-passthrough"/>`,
	}

	for _, expected := range expectedDefaults {
		if !strings.Contains(xml, expected) {
			t.Errorf("renderDomainXML() expected default element %q not found in XML:\n%s", expected, xml)
		}
	}
}

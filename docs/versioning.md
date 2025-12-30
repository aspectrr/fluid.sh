# Versioning Strategy

## Automatic Version Bumping

Every merged PR automatically triggers a release with the following logic:

### Default Behavior (No Labels)
```
0.0.0 → 0.0.1 → 0.0.2 → ... → 0.0.9 → 0.1.0 → 0.1.1 → ... → 0.1.9 → 0.2.0
```

- **Patch** increments from 0-9
- At patch 9, next PR bumps **minor** and resets patch to 0

### With PR Labels

#### `minor` label
```
0.5.3 → 0.6.0  (forces minor bump, resets patch)
```

#### `major` label
```
0.9.8 → 1.0.0  (manual major version bump)
```

#### `skip-release` label
```
No release is created for this PR
```

## Examples

| Current | PR Label | Next Version |
|---------|----------|--------------|
| 0.0.5   | (none)   | 0.0.6        |
| 0.0.9   | (none)   | 0.1.0        |
| 0.5.7   | minor    | 0.6.0        |
| 0.9.9   | (none)   | 0.10.0       |
| 0.9.9   | major    | 1.0.0        |

## Skip Release

Add the `skip-release` label to PRs that shouldn't trigger a release:
- Documentation-only changes
- CI/CD configuration updates
- Internal refactoring without user-facing changes

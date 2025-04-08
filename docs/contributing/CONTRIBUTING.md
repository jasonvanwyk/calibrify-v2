# Contributing to Calibrify

Thank you for your interest in contributing to Calibrify! This document provides guidelines and workflows for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing.

## How to Contribute

### 1. Setting Up Your Development Environment

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/calibrify-v2.git
   cd calibrify-v2
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Install Dependencies**
   ```bash
   # Copy environment variables
   cp .env.example .env

   # Start development environment
   docker-compose -f docker/development/docker-compose.dev.yml up --build
   ```

### 2. Making Changes

1. **Follow Code Style**
   - Python: Follow PEP 8
   - JavaScript: Follow our ESLint configuration
   - See [CODING_STANDARDS.md](../development/CODING_STANDARDS.md)

2. **Write Tests**
   - Add unit tests for new features
   - Ensure existing tests pass
   - Maintain or improve code coverage

3. **Update Documentation**
   - Update relevant documentation
   - Add inline comments for complex logic
   - Update API documentation if needed

### 3. Submitting Changes

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Follow our commit message convention:
   - `feat:` New features
   - `fix:` Bug fixes
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test updates
   - `chore:` Maintenance tasks

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Use our pull request template
   - Link related issues
   - Provide clear description of changes
   - Add screenshots for UI changes

### 4. Review Process

1. **Automated Checks**
   - CI pipeline will run tests
   - Code style checks
   - Security scans

2. **Code Review**
   - At least one maintainer review required
   - Address review comments
   - Keep discussions focused

3. **Final Steps**
   - Squash commits if requested
   - Rebase on main if needed
   - Update PR description if needed

## Development Guidelines

### 1. Code Quality

- Write self-documenting code
- Follow SOLID principles
- Keep functions focused and small
- Use meaningful variable names
- Add type hints in Python code

### 2. Testing

- Write unit tests for new code
- Include integration tests where needed
- Test edge cases
- Mock external services
- Aim for 85%+ coverage

### 3. Documentation

- Update README.md if needed
- Document new features
- Update API documentation
- Include examples
- Document breaking changes

### 4. Performance

- Consider scalability
- Optimize database queries
- Use caching appropriately
- Profile code when needed
- Consider bulk operations

## Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] CI checks passing
- [ ] No merge conflicts
- [ ] Reviewed by team member

## Getting Help

- Join our Discord server
- Check existing issues
- Ask in discussions
- Contact maintainers

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Invited to team meetings

## License

By contributing, you agree that your contributions will be licensed under the project's MIT license. 
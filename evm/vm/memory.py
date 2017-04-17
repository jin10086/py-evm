import itertools
import logging

from evm.validation import (
    validate_is_bytes,
    validate_length,
    validate_lte,
    validate_uint256,
)

from evm.utils.numeric import (
    ceil32,
)


class Memory(object):
    """
    EVM Memory
    """
    bytes = None
    logger = logging.getLogger('evm.vm.memory.Memory')

    def __init__(self):
        self.bytes = bytearray()

    def extend(self, start_position, size):
        if size == 0:
            return

        new_size = ceil32(start_position + size)
        if new_size <= len(self):
            return

        size_to_extend = new_size - len(self)
        self.bytes.extend(itertools.repeat(0, size_to_extend))

    def __len__(self):
        return len(self.bytes)

    def write(self, start_position, size, value):
        """
        Write `value` into memory.
        """
        if size:
            validate_uint256(start_position)
            validate_uint256(size)
            validate_is_bytes(value)
            validate_length(value, length=size)
            validate_lte(start_position + size, maximum=len(self))

            self.bytes = (
                self.bytes[:start_position] +
                bytearray(value) +
                self.bytes[start_position + size:]
            )

    def read(self, start_position, size):
        from eth_utils import encode_hex
        """
        Read a value from memory.
        """
        return bytes(self.bytes[start_position:start_position + size])
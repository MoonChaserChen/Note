package ink.akira.note.dao;

import ink.akira.note.po.PetDO;

public interface PetDAO {
    int deleteByPrimaryKey(Long id);

    int insert(PetDO record);

    int insertSelective(PetDO record);

    PetDO selectByPrimaryKey(Long id);

    int updateByPrimaryKeySelective(PetDO record);

    int updateByPrimaryKey(PetDO record);
}